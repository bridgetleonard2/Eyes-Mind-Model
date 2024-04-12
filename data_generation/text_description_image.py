import json
import base64
import requests

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
        "model": "gpt-4-vision-preview",
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

    print(response_json)
    if 'choices' in response_json and response_json['choices']:
        simple_response = response_json['choices'][0]['message']['content']
    else:
        simple_response = "no response"

    return simple_response


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


file_path = 'fine_tuning/training/uniqueWords.txt'
words = []

with open(file_path, 'r') as file:
    for line in file:
        word = line.strip()
        words.append(word)
print(words)

train_json = []

for index in range(len(words)):
    word = words[index]
    if word == "desire":
        text = "Describe what makes this person look like they have desire."
    else:
        text = f"Describe what makes this person look like they are {word}."

    image = f"{word}_2.jpg"

    response = get_response(text, 
                            "data_generation/data/adobe2/" + image)
    new_item = json_item(image, word, response, index)

    train_json.append(new_item)

with open("llava_hyak/adobe_dataset2/train/train_data.json", "w") as file:
    json.dump(train_json, file, indent=2)
