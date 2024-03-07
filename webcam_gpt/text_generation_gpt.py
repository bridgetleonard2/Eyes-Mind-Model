import json
import requests

api_key = '***REMOVED***'


def get_response(prompt):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers, json=payload)

    response_json = response.json()

    print(response_json)
    return response_json


file_path = 'uniqueWords.txt'
words = []

with open(file_path, 'r') as file:
    for line in file:
        word = line.strip()
        words.append(word)

# Test one description/prompt engineering
prompt = "Create a textual description of someone who looks regretful."

get_response(prompt)

text_description = {}

for description in words[28:]:
    text = f"Create a textual description of someone who looks {description}."
    print("Generating a description for someone who looks", description)
    response = get_response(text)
    text_description[description] = response

with open('text_descriptions.txt', 'w') as file:
    file.write(json.dumps(text_description))
