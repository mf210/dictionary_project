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

def get_data(phrase: str):
	# create payload based on phrase
	payload = {} 	
	splited_phrase = phrase.split()
	if len(splited_phrase) > 1:
		payload['selection'] = splited_phrase[0]
		payload['textAfterSelection'] = ' '.join(splited_phrase[1:])
	else:
		payload['selection'] = phrase
	# get data from api
	data = requests.request("POST", url, json=payload,
							headers=headers, params=querystring).json()
	# sort data
	result = {
		'phrase': phrase,
		'definitions': [],
		'examples': [],
		'antonyms': [],
		'synonyms': [],
		'Other Forms': set()
	}
	for item in data.get('items', []):
		result['antonyms'].extend(item.get('antonyms', []))
		result['synonyms'].extend(item.get('synonyms', []))
		for definition_obj in item.get('definitions', []):
			result['definitions'].append(definition_obj['definition'])
			result['examples'].extend(definition_obj.get('examples', []))
		# extrac the other forms of phrase 
		for inflectional_form in item.get('inflectionalForms', []):
			other_form = inflectional_form['forms'][0]
			if other_form:
				result['Other Forms'].add(other_form)

	result['Other Forms'] = list(result['Other Forms'])
	return result