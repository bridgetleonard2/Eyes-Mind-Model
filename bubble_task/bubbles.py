import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import base64
import requests
import re
import os
import sys
import sklearn.linear_model as lm
from tqdm import tqdm


def crop_image(image_path):
    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Image not found or path is incorrect")

    # Define the white pixel value threshold
    whitePixelValue = 254

    # Find rows and columns where all values are close to white
    whiteRows = np.all(img >= whitePixelValue, axis=1)
    whiteCols = np.all(img >= whitePixelValue, axis=0)

    # Find indices of first and last non-white rows and columns
    firstNonWhiteRow = np.where(~whiteRows)[0][0]
    lastNonWhiteRow = np.where(~whiteRows)[0][-1]
    firstNonWhiteCol = np.where(~whiteCols)[0][0]
    lastNonWhiteCol = np.where(~whiteCols)[0][-1]

    # Crop the image to remove white borders
    croppedImg = img[firstNonWhiteRow:lastNonWhiteRow+1,
                     firstNonWhiteCol:lastNonWhiteCol+1]

    # Display the original and cropped images for comparison
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(croppedImg, cmap='gray')
    plt.title('Cropped Image')
    plt.axis('off')

    plt.show()

    return croppedImg


def bubbles_test(image_path, num_bubbles=10, bubble_size=20, num_trials=500):
    # Load the grayscale image
    img = crop_image(image_path)
    if img.ndim == 3:  # Convert to grayscale if it is not
        img = img.mean(axis=2)
    img = img / 255  # Normalize image to [0, 1]

    imageSize = img.shape

    # Initialize response arrays
    responseMatrix = np.zeros((num_trials, imageSize[0] * imageSize[1]))
    responses = np.zeros(num_trials)

    for t in tqdm(range(num_trials)):
        # Generate sparse image with bubbles
        sparseImg = np.zeros(imageSize)
        mask = np.zeros(imageSize)
        for j in range(num_bubbles):
            x = np.random.randint(0, imageSize[1])
            y = np.random.randint(0, imageSize[0])
            X, Y = np.meshgrid(range(imageSize[1]), range(imageSize[0]))
            bubble = np.exp(-((X-x)**2 + (Y-y)**2) / (2*bubble_size**2))
            mask += bubble

        mask /= mask.max()  # Normalize the mask
        sparseImg = img * mask

        # If both eyes are partially visible response is correct
        if mask[60, 180] > 0.50 and mask[60, 60] > 0.50:
            response = 1
        else:
            response = 0
        responses[t] = response
        responseMatrix[t, :] = mask.ravel()

    # Calculate the mean response over the trials with positive responses
    filtered_responses = responseMatrix[responses > 0]
    if filtered_responses.size > 0:
        average_response = filtered_responses.mean(axis=0)
    else:
        average_response = np.zeros(imageSize[0] * imageSize[1])

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(sparseImg, cmap='gray')
    plt.axis('off')
    plt.title('Sparse Image')

    plt.subplot(1, 2, 2)
    plt.imshow(mask, cmap='gray')
    plt.axis('off')
    plt.title('Mask')
    plt.show()

    # Display the mean response image
    plt.imshow(average_response.reshape(imageSize), cmap='gray')
    plt.title('Average Response Image')
    plt.colorbar()
    plt.show()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_response(prompt, image_path):
    image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "top_p": 0.5,
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
                    "url": f"data:image/jpeg;base64,{image}"
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

    # Extracting the generated answer
    short_response = response_json['choices'][0]['message']['content']
    answer = re.findall(r'"([^"]*)"', short_response)

    print(answer)

    if answer:
        answer = answer[0]
    else:
        answer = 'None'

    # Remove period from answer if present
    answer = answer.replace(".", "")

    # Make answer lowercase
    answer = answer.lower()

    print(answer)
    return answer


def bubbles_gpt(image_path, answer, num_bubbles=10,
                bubble_size=20, num_trials=500):
    # Load the grayscale image
    img = crop_image(image_path)
    if img.ndim == 3:  # Convert to grayscale if it is not
        img = img.mean(axis=2)
    img = img / 255  # Normalize image to [0, 1]

    imageSize = img.shape

    # Initialize response arrays
    responseMatrix = np.zeros((num_trials, imageSize[0] * imageSize[1]))
    responses = np.zeros(num_trials)

    for t in tqdm(range(num_trials)):
        # Generate sparse image with bubbles
        sparseImg = np.zeros(imageSize)
        mask = np.zeros(imageSize)
        for j in range(num_bubbles):
            x = np.random.randint(0, imageSize[1])
            y = np.random.randint(0, imageSize[0])
            X, Y = np.meshgrid(range(imageSize[1]), range(imageSize[0]))
            bubble = np.exp(-((X-x)**2 + (Y-y)**2) / (2*bubble_size**2))
            mask += bubble

        mask /= mask.max()  # Normalize the mask
        sparseImg = img * mask

        filename = f'bubble_task/temp/sparse_image_trial_{t}.png'
        cv2.imwrite(filename, (sparseImg * 255).astype(np.uint8))

        # Call GPT-4 API:
        # Extract possible answers from image name
        # Ex image path: 01-playful-comforting-irritated-bored-300x175.jpg
        image_name = image_path.split("\\")[-1]
        # print(f"File Name: {image_name}")
        image_name = image_name.split(".")[0]
        # print(f"Without Extension: {image_name}")
        image_answers = image_name.split("-")[1:5]
        # print(f"Image Answers: {image_answers}")
        answers = ", ".join(image_answers)

        print(answers)

        prompt = f"Choose which word best describes what the person \
                in the picture is thinking or feeling. You may feel that \
                more than one word is applicable, but please choose \
                just one word, the word which you consider to be most \
                suitable. Your 4 choices are: {answers}"

        # Get response from GPT-4
        response = get_response(prompt, filename)

        # Check if response is correct
        if response == answer:
            response = 1
        else:
            response = 0
        responses[t] = response
        responseMatrix[t, :] = mask.ravel()

    # Delete contents in temp folder
    files = glob.glob('bubble_task/temp/*')
    for f in files:
        os.remove(f)

    # Calculate the mean response over the trials with positive responses
    filtered_responses = responseMatrix[responses > 0]
    if filtered_responses.size > 0:
        average_response = filtered_responses.mean(axis=0)
    else:
        average_response = np.zeros(imageSize[0] * imageSize[1])

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(sparseImg, cmap='gray')
    plt.axis('off')
    plt.title('Sparse Image')

    plt.subplot(1, 2, 2)
    plt.imshow(mask, cmap='gray')
    plt.axis('off')
    plt.title('Mask')
    plt.show()

    # Display the mean response image
    plt.imshow(average_response.reshape(imageSize), cmap='gray')
    plt.title('Average Response Image')
    plt.colorbar()
    plt.show()

    return responseMatrix, responses, imageSize


def linReg_analysis(responseMatrix, responses, imageSize):
    X = responseMatrix
    y = responses
    reg = lm.LinearRegression().fit(X, y)
    coef = reg.coef_

    # Plot coefficients to see which pixels are most important
    plt.imshow(coef.reshape(imageSize), cmap='coolwarm')
    plt.colorbar()
    plt.title('Linear Regression Coefficients')
    plt.show()


if __name__ == "__main__":
    # Set your OpenAI API key here
    api_key = ""

    if len(sys.argv) == 2:
        rmet_item = int(sys.argv[1])

        # Get item answer
        answers_file = 'task_materials/answers.txt'
        with open(answers_file, 'r') as file:
            answers = [line.strip() for line in file.readlines()]

        answer = answers[rmet_item - 1]

        # If rmet_item is single digit integer without leading zero
        if rmet_item < 10:
            rmet_item = f"0{rmet_item}"

        # Find image path based on item
        image_path_pattern = f"task_materials/regular/{rmet_item}*"
        image_path = glob.glob(image_path_pattern)[0]

        # Start with test
        # bubbles_test(image_path, num_trials=50)

        # Now GPT
        responseMatrix, responses, imageSize = bubbles_gpt(image_path, answer,
                                                           num_trials=50)

        # Linear Regression Analysis
        linReg_analysis(responseMatrix, responses, imageSize)
    else:
        print("Usage: python bubbles.py <image_path>")
        sys.exit(1)
