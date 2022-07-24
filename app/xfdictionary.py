import os
import requests


url = f"https://{os.environ['X_RAPIDAPI_HOST']}/v1/dictionary"
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": os.environ['X_RAPIDAPI_KEY'],
	"X-RapidAPI-Host":  os.environ['X_RAPIDAPI_HOST']
}
USA_PRONUNC_SIGNS = ["(General American)", "<i>noun</i>", "<i>verb</i>" , "(US)"]


def get_us_pronunciation(data: dict, word: str):
	for pronunciation in data.get('pronunciations', []):
		for entry in pronunciation.get('entries', []):
			if entry['entry'] == word:
				for textual in entry.get('textual', []):
					us_pron = textual['pronunciation']
					if any(x in us_pron for x in USA_PRONUNC_SIGNS) or ('(' not in us_pron):
						return us_pron

def get_word_frequencies(data: dict, word: str):
	res = {}
	for word_frequency in data.get('wordFrequencies', []):
		if word_frequency['word'] == word:
			for frequency in word_frequency.get('frequencies', []):
				res[frequency['partOfSpeech']] = frequency['frequencyBand']
	return res

def split_list_strings(items: list[str]):
	res = []
	for item in items:
		res.extend(item.split(','))
	return res

def sort_data(data: dict, word: str):
	result = {}
	word_frequencies = get_word_frequencies(data, word)
	us_pronunciation = get_us_pronunciation(data, word)

	for item in data.get('items', []):
		part_of_speech = item.get('partOfSpeech')
		item_data = {
			'word': word,
			'wordFamily': [],
			'antonyms': split_list_strings(item.get('antonyms', [])),
			'synonyms': split_list_strings(item.get('synonyms', [])),
			'definitions': item.get('definitions', [])
		}
		
		item_data['pronunciation'] = us_pronunciation
		item_data['frequency'] = word_frequencies.get(part_of_speech)

		for inflectional_form in item.get('inflectionalForms', []):
			other_form = inflectional_form['forms'][0]
			if other_form:
				item_data['wordFamily'].append(other_form)

		result[part_of_speech] = item_data
		
	result['word'] = word
	return result

def get_data(word: str):
	# create payload based on word
	payload = {} 	
	splited_word = word.split()
	if len(splited_word) > 1:
		payload['selection'] = splited_word[0]
		payload['textAfterSelection'] = ' '.join(splited_word[1:])
	else:
		payload['selection'] = word
	# get response from api
	data = requests.request("POST", url, json=payload, headers=headers).json()
	return sort_data(data, word)


if __name__ == '__main__':
	from pprint import pprint
	pprint(get_data('good'))