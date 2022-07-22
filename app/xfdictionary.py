import os
import requests

url = f"https://{os.environ['X_RAPIDAPI_HOST']}/v1/dictionary"
querystring = {
	"antonyms":"true",
	"audioFileLinks":"false",
	"pronunciations":"false",
	"relatedWords":"false",
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": os.environ['X_RAPIDAPI_KEY'],
	"X-RapidAPI-Host":  os.environ['X_RAPIDAPI_HOST']
}

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
	data = requests.request("POST", url, json=payload,
							headers=headers, params=querystring).json()
	# sort data
	result = {
		'word': word,
		'definitions': [],
		'examples': [],
		'antonyms': [],
		'meanings': [],
		'forms': set()
	}
	for item in data.get('items', []):
		result['antonyms'].extend(item.get('antonyms', []))
		result['meanings'].extend(item.get('synonyms', []))
		for definition_obj in item.get('definitions', []):
			result['definitions'].append(definition_obj['definition'])
			result['examples'].extend(definition_obj.get('examples', []))
		# extrac the other forms of word 
		for inflectional_form in item.get('inflectionalForms', []):
			other_form = inflectional_form['forms'][0]
			if other_form:
				result['forms'].add(other_form)

	result['forms'] = list(result['forms'])
	return result