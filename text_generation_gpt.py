import glob
import requests
import re

api_key = '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'


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


file_path = 'uniqueWords.txt'
words = []

with open(file_path, 'r') as file:
    for line in file:
        words.append(line)

responses = {}

# Test one description/prompt engineering
prompt = "Create a textual description of someone who looks regretful."

get_response(prompt)


#for index in range(len(questions)):
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
