import requests
import os


url = f"https://{os.environ['X_RAPIDAPI_HOST']}/v1/dictionary"

querystring = {"selection":"successfully","textAfterSelection":"completed their project.","textBeforeSelection":"They"}

payload = {
	"selection": "successfully",
	"textAfterSelection": "completed their project.",
	"textBeforeSelection": "They"
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": os.environ['X_RAPIDAPI_KEY'],
	"X-RapidAPI-Host":  os.environ['X_RAPIDAPI_HOST']
}

response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

print(response.text)