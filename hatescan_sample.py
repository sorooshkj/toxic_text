import requests
import json

'''
Get toxic score for the text from Hatescan API.
The API supports swedish and english language text.
For swedish text use 'sv' parameter and 'en' for english text.
If flag_detect_lang is set to True, the model can automatically detect the language of the text.
'''
def get_toxic_probability(text, language, flag_detect_lang):
    # adding \ infront of " in the text
    text = text.replace('"', '\\"')

    payload = '{"text": "' + text + '", "language": "' + language +'" , "flag_detect_lang": "' + flag_detect_lang +'"}'

    json_payload =json.loads(payload, strict=False)

    headers={"Content-Type": "application/json; charset=utf-8"}

    # Hatescan API url
    api_hatescan_url = 'https://detect.hatescan.com/predict/toxic'

    # sending post request to the API
    hatescan_response = requests.post(api_hatescan_url, headers=headers, json=json_payload)

    # return toxic and threat probability
    return hatescan_response.json()


if __name__ == '__main__':
    # sampel text
    text = "Jag litar inte på saker jag inte själv vet är sanna.."
    # text language
    language = 'sv'
    # automatic language detection flag
    flag_detect_language = 'False'

    toxic_score = get_toxic_probability(text, language, flag_detect_language)
    print(toxic_score)