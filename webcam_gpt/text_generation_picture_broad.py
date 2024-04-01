import glob
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


file_path = 'fine_tuning/training/uniqueWords.txt'
words = []

with open(file_path, 'r') as file:
    for line in file:
        word = line.strip()
        words.append(word)
print(words)

responses = []

# for index in range(len(questions)):
index = 0

for index in range(len(words)):
    word = words[index]
    print(word)
    if word == "desire":
        text = "Describe what makes this person look like they have desire."
    else:
        text = f"Describe what makes this person look like they are {word}."
    pattern = f"fine_tuning/training/Firefly/*{word}.jpg"

    # Use glob to find matching filenames
    image_path = glob.glob(pattern)[0]
    print(image_path)

    response = get_response(text, image_path)
    print(response)

    responses.append([word, response])

with open("fine_tuning/training/descriptions.txt", "w") as file:
    for response in responses:
        file.write(f"{response[0]}: {response[1]}\n")
