import requests
import json
import pandas as pd

def get_toxic_threat_probability(text, language, flag_detect_lang):
    # adding \ infront of " in the text
    text = text.replace('"', '\\"')

    payload = '{"text": "' + text + '", "language": "' + language +'" , "flag_detect_lang": "' + flag_detect_lang +'"}'

    json_payload =json.loads(payload, strict=False)

    headers={"Content-Type": "application/json; charset=utf-8"}

    # Hatescan API url
    api_hatescan_url = 'https://detect.hatescan.com/predict/toxic'

    # sending post request to the API
    hatescan_response = requests.post(api_hatescan_url, headers=headers, json=json_payload)

    # return toxic probability
    return hatescan_response.json()


def process_posts(input_file, output_file, language, flag_detect_lang):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Select the first column regardless of its name
    posts = df.iloc[:, 0].tolist()

    results = []

    for post in posts:
        score = get_toxic_threat_probability(post, language, flag_detect_lang)
        toxic_score = score.get('toxic_predictions', 'N/A')
        threat_score = score.get('threat_predictions', 'N/A')

        print(f"Toxic Score: {toxic_score}\nThreat Score: {threat_score}\n")
        results.append({
            'post': post,
            'toxic_score': toxic_score,
            'threat_score': threat_score
        })

    # Convert the results list into a DataFrame
    result_df = pd.DataFrame(results)

    # Save the results to a new Excel file
    result_df.to_excel(output_file, index=False)


if __name__ == '__main__':
    # input_file = 'blackpill-5000.xlsx'
    # output_file = 'processed_blackpill_5000.xlsx'
    input_file = 'files/Annotation_file_ML.xlsx'
    output_file = 'files/Annotation_file_ML_Score.xlsx'
    language = 'en'
    flag_detect_language = 'False'

    # Process the posts and save the results
    process_posts(input_file, output_file, language, flag_detect_language)
    print(f"Results saved to {output_file}")
