import tkinter as tk
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterFace:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = tk.Tk()
        self.window.title("Quiz Game")
        self.window.config(background=THEME_COLOR, padx=20, pady=20)

        # Scoreboard
        self.score_board = tk.Label(
            text=f"Score: 0",
            fg="white",
            background=THEME_COLOR,
            font=("Arial", 10, "bold"),
        )
        self.score_board.grid(row=0, column=1)

        # Canvas
        self.canvas = tk.Canvas(width=600, height=600, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=2, pady=20, sticky="nsew")
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        self.question_text = self.canvas.create_text(
            300, 300, fill=THEME_COLOR, font=("Arial", 20, "italic"), anchor="center"
        )

        # Update canvas text on window resize
        self.canvas.bind("<Configure>", self.resize_canvas)

        self.correct_image = tk.PhotoImage(file="images/true.png")
        self.true_button = tk.Button(image=self.correct_image, command=self.CheckTrue)
        self.true_button.grid(row=2, column=0)

        self.uncorrect_image = tk.PhotoImage(file="images/false.png")
        self.false_button = tk.Button(
            image=self.uncorrect_image, command=self.CheckFalse
        )
        self.false_button.grid(row=2, column=1)

        self.get_next_question()

        self.window.mainloop()

    def resize_canvas(self, event):
        # Make sure the text is always centered
        self.canvas.coords(self.question_text, event.width / 2, event.height / 2)
        # Update the width of the text
        self.canvas.itemconfig(self.question_text, width=event.width * 0.8)

    def get_next_question(self):
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(
                self.question_text,
                text=f"{self.quiz.current_question.difficulty.capitalize()}\n\n{q_text}",
            )
            self.score_board.config(text=f"Score: {self.quiz.score}")
        else:
            # Show score and disable buttons after all questions have been asked
            self.score_board.config(
                text=f"Score: {self.quiz.score} / {self.quiz.question_number}"
            )
            self.canvas.itemconfig(
                self.question_text, text="You've reached the end of the quiz"
            )
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def CheckTrue(self):
        answer = self.quiz.check_answer("True")
        self.give_feedback(answer)

    def CheckFalse(self):
        answer = self.quiz.check_answer("False")
        self.give_feedback(answer)

    def give_feedback(self, answer):
        if answer:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")

        def orginal_color():
            self.canvas.config(bg="white")
            self.get_next_question()

        self.window.after(1000, orginal_color)
