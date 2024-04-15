import base64
import requests
import pandas as pd
import json
from sklearn.model_selection import train_test_split

api_key = ''


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_response(prompt, image_path):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
             "role": "user",
             "content": [
                {
                 "type": "text",
                 "text": prompt
                },
                {
                 "type": "image_url",
                 "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                 }
                }
             ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers, json=payload)

    response_json = response.json()

    # print(response_json)
    if 'choices' in response_json and response_json['choices']:
        simple_response = response_json['choices'][0]['message']['content']
    else:
        simple_response = "no response"

    # print(simple_response)
    return simple_response


train_data = pd.read_csv('llava_hyak/ferGPT_dataset/train_data.csv')
train_json_data, val_json_data = train_test_split(train_data, test_size=0.2,
                                                  random_state=42)


def json_item(image, word, answer, index):
    new_item = {
        "id": f"{index:07}",  # Formats index leading zeros
        "image": image,
        "conversations": [
            {
                "from": "human",
                "value": "<image>\nWhat does this person look like they are thinking or feeling?"
            },
            {
                "from": "gpt",
                "value": answer
            }
        ]
    }
    return new_item


train_json = []

for index, row in train_json_data.iterrows():
    image = row['filename']
    word = row['emotion_words']
    answer = get_response(f"Describe what makes this person look like they are {word}.",
                          'llava_hyak/ferGPT_dataset/images/' + image)
    new_item = json_item(image, word, answer, index)
    print(new_item)
    train_json.append(new_item)

with open('llava_hyak/ferGPT_dataset/train/train_data.json', 'w') as f:
    json.dump(train_json, f, indent=2)

val_json = []

for index, row in val_json_data.iterrows():
    image = row['filename']
    word = row['emotion_words']
    answer = get_response(f"Describe what makes this person look like they are {word}.",
                          'llava_hyak/ferGPT_dataset/images/' + image)
    new_item = json_item(image, word, answer, index)
    print(new_item)
    val_json.append(new_item)

with open('llava_hyak/ferGPT_dataset/validation/val_data.json', 'w') as f:
    json.dump(val_json, f, indent=2)
