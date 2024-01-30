import glob
import base64
import requests
import re

api_key = '*enter your key here*'

subject = 'P001'  # Choose images to evaluate


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

    # Extracting the generated answer
    short_response = response_json['choices'][0]['message']['content']
    answer = re.findall(r'"([^"]*)"', short_response)

    print(answer)

    if answer:
        answer = answer[0]
    else:
        answer = 'None'

    print(answer)
    return answer


file_path = 'task_materials/wordOptions.txt'
questions = []

with open(file_path, 'r') as file:
    for line in file:
        words = line.strip().split()
        question = f"Question {len(questions) + 1}"
        answers = words
        questions.append((question, answers))
print(questions)

responses = {}

# for index in range(len(questions)):
index = 0
question, answers = questions[index]
print(question)
text = f"Choose which word best describes what \
    the person in the picture is thinking or feeling. \
        You may feel that more than one word is applicable, \
            but please choose just one word, the word \
                which you consider to be most suitable. \
                    Your 4 choices are:, {answers}"

folder = subject  # Change to relevant subject
pattern = f"{folder}/{index + 1:02d}*.png"

# Use glob to find matching filenames
image_path = glob.glob(pattern)[0]
print(image_path)

response = get_response(text, image_path)

responses[question] = response

with open(subject + "_gpt.txt", "w") as file:
    for question, response in responses.items():
        file.write(f"{question}: {response}\n")
