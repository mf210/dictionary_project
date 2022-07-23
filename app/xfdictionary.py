import os
import requests

url = f"https://{os.environ['X_RAPIDAPI_HOST']}/v1/dictionary"
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": os.environ['X_RAPIDAPI_KEY'],
	"X-RapidAPI-Host":  os.environ['X_RAPIDAPI_HOST']
}
USA_PRONUNCIATION_SIGNS = ["(General American)", "<i>noun</i>", "<i>verb</i>"]


def is_us_pronunc(pronunc: str):
	if any(x in pronunc for x in USA_PRONUNCIATION_SIGNS) or ('(' not in pronunc):
		return True

def gen_dict_extract(key, var):
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    if is_us_pronunc(result):
                        yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        if is_us_pronunc(result):
                            yield result

def get_data(word: str):
	# create payload based on word
	payload = {} 	
	splited_word = word.split()
	if len(splited_word) > 1:
		payload['selection'] = splited_word[0]
		payload['textAfterSelection'] = ' '.join(splited_word[1:])
	else:
		payload['selection'] = word
	# get data from api
	data = requests.request("POST", url, json=payload, headers=headers).json()
	# sort data
	result = {
		'word': word,
		'definitions': [],
		'wordFrequencies': data.get('wordFrequencies', []),
		'pronunciations': list(
			gen_dict_extract('pronunciation', data.get('pronunciations',[{}])[0])
		)
	}
	for item in data.get('items', []):
		current_definition = {
			'partOfSpeech': [item.get('partOfSpeech', None)],
			'antonyms': item.get('antonyms', []),
			'synonyms': item.get('synonyms', []),
			'definitions': [],
			'examples': [],
			'forms': []
		}
		# extract definitions and examples of word
		for definition_obj in item.get('definitions', []):
			current_definition['definitions'].append(definition_obj['definition'])
			current_definition['examples'].extend(definition_obj.get('examples', []))
		# extract other forms of word
		for inflectional_form in item.get('inflectionalForms', []):
			other_form = inflectional_form['forms'][0]
			if other_form:
				current_definition['forms'].append(other_form)

		result['definitions'].append(current_definition)
	return result

if __name__ == '__main__':
	print(get_data('word'))