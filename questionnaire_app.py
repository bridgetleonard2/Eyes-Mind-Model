
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk, ImageFilter # Functions for image loading and displaying
import glob # Photo file path finder

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
        self.question_label = tk.Label(self.root, text="", font=("Helvetica", 16))
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
        self.prev_button = tk.Button(self.root, text="Previous", command=self.prev_question)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_question)
        self.next_button.pack(side=tk.RIGHT, padx=10)

    def display_question(self, index):
        # Clear previous answers
        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        if index < len(self.questions):
            question, answers = self.questions[index]

            self.question_label.config(text=question)

            # Establish condition -- change downstream of the image directory
            if index < 12:
                folder = "regular"
            elif 12 <= index < 24:
                folder = "upsidedown"
            elif 24 <= index < 36:
                folder = "scrambled"

            # Create a pattern for globbing
            pattern = f"{folder}/{index + 1:02d}*.jpg"

            # Use glob to find matching filenames
            image_path = glob.glob(pattern)[0]
            print(image_path)
            # Load and display image
            try:
                image = Image.open(image_path)
                image = image.resize((600, 350), Image.Resampling.LANCZOS)  # Adjust the size as needed
                self.photo = ImageTk.PhotoImage(image)  # Make photo an instance variable
                self.image_label.config(image=self.photo)
            except FileNotFoundError:
                messagebox.showwarning("Image Not Found", f"Image file not found: {image_path}")
                self.image_label.config(image=None)

            for answer in answers:
                btn = tk.Button(self.answers_frame, text=answer, command=lambda a=answer: self.record_response(question, a))
                btn.pack(side=tk.LEFT, padx=10)

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
            messagebox.showinfo("Completed", "Questionnaire completed. Responses saved.")

    def save_responses(self):
        file_name = simpledialog.askstring("Save File", "Enter file name to save responses:", parent=self.root)
        if file_name:
            with open(file_name + ".txt", "w") as file:
                for question, response in self.responses.items():
                    file.write(f"{question}: {response}\n")

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
    # Replace 'your_file_path_here.txt' with the path to your file containing the words
    questions = read_questions('C:\\Users\\Bridget Leonard\\Desktop\\eyes_emotion\\wordOptions.txt')

    # Create the GUI application
    root = tk.Tk()
    app = QuestionnaireApp(root, questions)
    root.mainloop()
