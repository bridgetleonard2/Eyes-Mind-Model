import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
import base64
import requests
import re
import os
from transformers import pipeline


class QuestionnaireApp:
    def __init__(self, root, questions):
        self.root = root
        self.questions = questions
        self.responses = {}
        self.gpt_response = {}
        self.llava_response = {}
        self.current_question_index = -1
        self.participant_code = ""
        self.api_key = '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'

        self.setup_ui()

    def setup_ui(self):
        self.root.title("Questionnaire Score Sheet")

        # Label for displaying the question
        self.question_label = tk.Label(self.root, text="",
                                       font=("Helvetica", 16))
        self.question_label.pack(pady=20)

        # Frame for answer buttons
        self.answers_frame = tk.Frame(self.root)
        self.answers_frame.pack(pady=10)

        # Navigation buttons
        self.prev_button = tk.Button(self.root, text="Previous",
                                     command=self.prev_question)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.root, text="Next",
                                     command=self.next_question)
        self.next_button.pack(side=tk.RIGHT, padx=10)

        self.capture_button = tk.Button(self.root, text="Capture Image",
                                        command=self.capture_and_crop)
        self.capture_button.pack(pady=10)

        # Initialize the questionnaire
        self.display_question(self.current_question_index)

    def display_question(self, index):
        # Clear previous answers
        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        if index < 0:
            # Entry widget for participant code
            self.participant_code_label = tk.Label(self.root,
                                                   text="Participant Code:")
            self.participant_code_label.pack(pady=10)

            self.participant_code_entry = tk.Entry(self.root)
            self.participant_code_entry.pack(pady=5)
        elif index < len(self.questions):
            question, answers = self.questions[index]

            self.participant_code_label.pack_forget()
            self.participant_code_entry.pack_forget()

            self.question_label.config(text=question)
            for answer in answers:
                btn = tk.Button(self.answers_frame, text=answer,
                                command=lambda a=answer:
                                self.record_response(question, a))
                btn.pack(side=tk.LEFT, padx=10)

    def record_response(self, question, answer):
        self.responses[question] = answer

    def prev_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.display_question(self.current_question_index)

    def next_question(self):
        if self.current_question_index == -1:
            # Check if participant code is entered
            participant_code = self.participant_code_entry.get()
            if not participant_code:
                messagebox.showerror("Error",
                                     "Please enter a participant code.")
                return

        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.display_question(self.current_question_index)
        else:
            self.save_responses()
            messagebox.showinfo("Completed", "Questionnaire completed. \
                                Responses saved.")

    def save_responses(self):
        file_name = simpledialog.askstring("Save File", "Enter file name to \
                                           save responses:", parent=self.root)
        if file_name:
            with open(os.path.join("data", file_name + ".txt"), "w") as file:
                for question, response in self.responses.items():
                    file.write(f"{question}: {response}\n")
            with open(os.path.join("data", file_name + "_gpt.txt")) as file:
                for question, response in self.gpt_response.items():
                    file.write(f"{question}: {response}\n")

    def capture_and_crop(self):
        # Take webcam picture and save the image path
        img_path = self.im_capture()

        # Get cropped eyes image
        base64_img_path = self.eye_crop(img_path)

        self.gpt_analyze(base64_img_path)
        # self.llava_analyze(base64_img_path)

    def im_capture(self):
        # intialize the webcam and pass a constant which is 0
        cam = cv2.VideoCapture(0)

        # title of the app
        cv2.namedWindow('python webcam screenshot app')

        # let's assume the number of images gotten is 0
        img_counter = 0

        # while loop
        while True:
            # intializing the frame, ret
            ret, frame = cam.read()
            # if statement
            if not ret:
                print('failed to grab frame')
                break
            # the frame will show with the title of test
            cv2.imshow('Take photo with spacebar, once done hit escape', frame)
            # to get continuous live video feed from my laptops webcam
            k = cv2.waitKey(1)
            # if the escape key is been pressed, the app will stop
            if k % 256 == 27:
                print('escape hit, closing the app')
                break
            # if the spacebar key is been pressed
            # screenshots will be taken
            elif k % 256 == 32:
                # the format for storing the images scrreenshotted
                img_name = f'opencv_frame_{img_counter}.png'
                # saves the image as a png file
                cv2.imwrite(img_name, frame)
                print('screenshot taken')
                # the number of images automaticallly increases by 1
                img_counter += 1

        # release the camera
        cam.release()

        # stops the camera window
        cv2.destroyAllWindows()

        return img_name

    def eye_crop(self, image_path):
        original_image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                            'haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(gray_image, scaleFactor=1.3,
                                            minNeighbors=5)

        # Assuming there are at least two detected eyes
        if len(eyes) >= 2:
            # Sort the eyes based on x-coordinate
            eyes = sorted(eyes, key=lambda x: x[0])

            # Consider the leftmost and rightmost eyes as a pair
            left_eye, right_eye = eyes[:2]

            # Extract coordinates for the bounding box
            x_left, y_left, w_left, h_left = left_eye
            x_right, y_right, w_right, h_right = right_eye

            # Combine the bounding boxes to include both eyes
            x = min(x_left, x_right)
            y = min(y_left, y_right)
            w = max(x_left + w_left, x_right + w_right) - x
            h = max(y_left + h_left, y_right + h_right) - y

            # Add some padding around the eye pair
            padding = 5
            x -= padding
            y -= padding
            w += 2 * padding
            h += 2 * padding

            # Ensure that the cropped region is within the image boundaries
            x = max(0, x)
            y = max(0, y)
            w = min(original_image.shape[1] - x, w)
            h = min(original_image.shape[0] - y, h)

            # Crop the image to the eye pair region
            cropped_image = original_image[y:y + h, x:x + w]

            # Display the original and cropped images (optional)
            cv2.imshow('Original Image', original_image)
            cv2.imshow('Cropped Image', cropped_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # Modify file_path to include the index and word names
            participant_code = self.participant_code_entry.get()

            # create participant image folder if doesn't exist
            if not os.path.exists(participant_code):
                os.mkdir(participant_code)

            index = self.current_question_index + 1
            words = '_'.join(self.questions[self.current_question_index]
                             [1][:4])
            file_path = os.path.join(participant_code,
                                     f'{index:02d}-{words}.png')
            cv2.imwrite(file_path, cropped_image)

            # Save the cropped image
            cv2.imwrite(file_path, cropped_image)

            # Delete original image
            if os.path.exists(image_path):
                os.remove(image_path)

                # Encode the cropped image to base64
                base64_image = self.encode_image(cropped_image)

                return base64_image
            else:
                print(f"File {image_path} not found.")
        else:
            print("At least two eyes are required for eye pair detection.")

    def encode_image(self, image):
        _, buffer = cv2.imencode('.png', image)
        return base64.b64encode(buffer).decode('utf-8')

    def gpt_analyze(self, base64_image):
        print('ChatGPT is analyzing the image...')
        question, answers = self.questions[self.current_question_index]

        prompt = f"Choose which word best describes what \
            the person in the picture is thinking or feeling based \
                on just their eyes alone. \
                You may feel that more than one word is applicable, \
                    but please choose just one word, the word \
                    which you consider to be most suitable. \
                        Your 4 choices are:, {answers}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
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
        if 'choices' in response_json:
            # Extracting the generated answer
            short_response = response_json['choices'][0]['message']['content']
            answer = re.findall(r'"([^"]*)"', short_response)

            if answer:
                answer = answer[0]
            else:
                answer = 'None'

            print(answer)
            # Record response
            self.gpt_response[question] = answer
        else:
            print(response_json)

    # def llava_analyze(self, base64_image):
    #     print("Llava is analyzing the image...")
    #     pipe = pipeline("image-to-text", model="llava-hf/llava-1.5-13b-hf")
    #     question, answers = self.questions[self.current_question_index]

    #     image = base64_image
    #     prompt = f'''USER: <image>
    #         Choose which word best describes what the person in the picture is
    #         thinking or feeling based on just their eyes alone.
    #         You may feel that more than one word is applicable,
    #         but please choose just one word, the word
    #         which you consider to be most suitable.
    #         Your 4 choices are: {answers}
    #         ASSISTANT:'''

    #     outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})
    #     result = [line.split(':')[-1].strip() for line in outputs[0]['generated_text'].split('\n')][-1]

    #     if result is None:
    #         print('No response given')
    #     else:
    #         print(result)
    #     # Record response
    #     self.llava_response[question] = result


# Read the questions from a file
def read_questions(file_path):
    questions = []
    with open(file_path, 'r') as file:
        for line in file:
            words = line.strip().split()
            question = f"Question {len(questions) + 1}"
            answers = words + ["refuse", "no answer"]
            questions.append((question, answers))
    return questions


if __name__ == "__main__":
    # Replace 'your_file_path_here.txt' with the path to your file
    # containing the words
    home_directory = os.path.expanduser("~")

    path_to_questions = os.path.join(home_directory, 'Desktop\\eyes_emotion\\task_materials\\wordOptions.txt')
    questions = read_questions(path_to_questions)

    # Create the GUI application
    root = tk.Tk()
    app = QuestionnaireApp(root, questions)
    root.mainloop()
