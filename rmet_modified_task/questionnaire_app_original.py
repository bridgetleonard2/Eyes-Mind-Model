
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk  # Image loading and displaying
import glob  # Photo file path finder
import os


class QuestionnaireApp:
    def __init__(self, root, questions):
        self.root = root
        self.questions = questions
        self.responses = {}
        self.current_question_index = 0
        self.photo = None  # Initialize self.photo as an attribute

        self.setup_ui()

    def setup_ui(self):
        self.root.title("Questionnaire Score Sheet")

        # Label for displaying the question
        self.question_label = tk.Label(self.root, text="",
                                       font=("Helvetica", 16))
        self.question_label.pack(pady=20)


        # Label for displaying the image
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=20)

        # Frame for answer buttons
        self.answers_frame = tk.Frame(self.root)
        self.answers_frame.pack(pady=10)

        # Initialize the questionnaire
        self.display_question(self.current_question_index)

        # Navigation buttons
        # self.prev_button = tk.Button(self.root, text="Previous",
        #                              command=self.prev_question)
        # self.prev_button.pack(side=tk.LEFT, padx=10)

        # self.next_button = tk.Button(self.root, text="Next",
        #                              command=self.next_question)
        # self.next_button.pack(side=tk.RIGHT, padx=10)

    def display_question(self, index):
        # Clear previous answers
        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        # Create an all-white image
        white_image = Image.new('RGB', (600, 350), 'white')
        self.photo = ImageTk.PhotoImage(white_image)
        self.image_label.config(image=self.photo)

        if index < len(self.questions):
            question, answers = self.questions[index]

            self.question_label.config(text=question)

            # Establish condition -- change downstream of the image directory
            folder = 'regular'

            # Create a pattern for globbing
            pattern = f"task_materials/{folder}/{index + 1:02d}*.jpg"

            # Use glob to find matching filenames
            image_path = glob.glob(pattern)[0]

            # Load and display image after 3 seconds
            self.root.after(500, self.update_image, image_path)

            for answer in answers:
                btn = tk.Button(self.answers_frame, text=answer,
                                command=lambda a=answer:
                                self.record_response(question, a))
                btn.pack(side=tk.LEFT, padx=10)

    def update_image(self, image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((600, 350), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.photo)
        except FileNotFoundError:
            messagebox.showwarning("Image Not Found",
                                   f"Image file not found: {image_path}")
            self.image_label.config(image=None)
        # Schedule the next question after 3 seconds
        self.root.after(10000, self.display_next_question)

        # Clear existing answer buttons
        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        # Display answer buttons
        question, answers = self.questions[self.current_question_index]
        for answer in answers:
            btn = tk.Button(self.answers_frame, text=answer,
                            command=lambda a=answer:
                            self.record_response(question, a))
            btn.pack(side=tk.LEFT, padx=10)

    def display_next_question(self):
        # Record a response of "no response" if no answer has been given
        question, answers = self.questions[self.current_question_index]
        if question not in self.responses:
            self.record_response(question, "no response")

        # Move to the next question
        self.next_question()

    def record_response(self, question, answer):
        self.responses[question] = answer

    def prev_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.display_question(self.current_question_index)

    def next_question(self):
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
            with open(os.path.join("rmet_modified_task/data/original/", file_name + ".txt"), "w") as file:
                for question, response in self.responses.items():
                    file.write(f"{question}: {response}\n")
            # Close the window after saving responses
            self.root.destroy()


# Read the questions from a file
def read_questions(file_path):
    questions = []
    with open(file_path, 'r') as file:
        for line in file:
            words = line.strip().split()
            question = f"Question {len(questions) + 1}"
            answers = words
            questions.append((question, answers))
    return questions


if __name__ == "__main__":
    # Replace 'your_file_path_here.txt' with the path to your file containing
    # the words
    home_directory = os.path.expanduser("~")

    questions = read_questions(os.path.join(home_directory, 'Desktop'
                               '\\Eyes-Mind-Model\\task_materials\\wordOptions.txt'))

    # Create the GUI application
    root = tk.Tk()
    app = QuestionnaireApp(root, questions)
    root.mainloop()
