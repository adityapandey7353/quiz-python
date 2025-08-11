import tkinter as tk
from tkinter import messagebox
import time

# --- UI Constants for styling ---
THEME_COLOR = "#375362" # A dark bluish-gray
CORRECT_COLOR = "#00FF00" # A vibrant green for correct answers (changed to pure green for visibility)
WRONG_COLOR = "#e74c3c"  # A distinct red for wrong answers
FEEDBACK_DELAY_MS = 2000 # How long the green/red feedback stays (in milliseconds)
TIMER_DURATION_SECONDS = 15 # Time allowed per question

class QuizInterface:
    def __init__(self, quiz_brain):
        self.quiz = quiz_brain
        self.window = tk.Tk()
        self.window.title("Python Quiz App")
        self.window.config(padx=40, pady=40, bg=THEME_COLOR) # Increased padding, theme color background

        # Score Label
        self.score_label = tk.Label(
            text=f"Score: 0/{self.quiz.question_number}",
            fg="white", # White text
            bg=THEME_COLOR, # Theme color background
            font=("Arial", 14, "bold") # Slightly larger font
        )
        self.score_label.grid(row=0, column=1, pady=(0, 20), sticky="e") # Top right, sticky to east (right)

        # Timer Label
        self.timer_label = tk.Label(
            text="Time: --",
            fg="white",
            bg=THEME_COLOR,
            font=("Arial", 14, "bold")
        )
        self.timer_label.grid(row=0, column=0, pady=(0, 20), sticky="w") # Top left, sticky to west (left)

        # Question Canvas (where the question text is displayed)
        self.canvas = tk.Canvas(width=400, height=250, bg="white", highlightthickness=0, bd=0) # Removed border
        self.question_text = self.canvas.create_text(
            200, 125, # Center of canvas
            width=360, # Wrap text within this width
            text="Some Question Text",
            fill=THEME_COLOR, # Dark bluish-gray text
            font=("Arial", 18, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=40) # Spans both columns, more vertical padding

        # Option Buttons (using text buttons with improved styling)
        self.true_button = tk.Button(
            text="True",
            width=15, # Increased width
            height=2,
            font=("Arial", 16, "bold"), # Larger, bolder font for buttons
            bg=CORRECT_COLOR, # Green background
            fg="white", # White text
            activebackground=CORRECT_COLOR, # Keep background color on click
            activeforeground="white",
            relief="raised", # Raised effect for buttons
            bd=3, # Border for button
            command=lambda: self.check_answer("True")
        )
        self.true_button.grid(row=2, column=0, pady=(20, 0), padx=(0, 10)) # Added some padding between buttons

        self.false_button = tk.Button(
            text="False",
            width=15, # Increased width
            height=2,
            font=("Arial", 16, "bold"), # Larger, bolder font for buttons
            bg=WRONG_COLOR, # Red background
            fg="white", # White text
            activebackground=WRONG_COLOR,
            activeforeground="white",
            relief="raised",
            bd=3,
            command=lambda: self.check_answer("False")
        )
        self.false_button.grid(row=2, column=1, pady=(20, 0), padx=(10, 0)) # Added some padding between buttons

        self.user_answer_entry = None # Placeholder if we add text input later

        # Timer variables initialization (Crucial to define BEFORE calling get_next_question)
        self.timer_duration = TIMER_DURATION_SECONDS # Use the constant
        self.current_time_left = self.timer_duration
        self.timer_id = None # To store the after() id for stopping the timer

        # Load the first question and start the timer immediately
        self.get_next_question()
        self.start_timer()

        # Start the Tkinter event loop - this keeps the window open and responsive
        self.window.mainloop()

    def get_next_question(self):
        """
        Fetches the next question from the quiz brain and updates the UI.
        Resets the canvas color and timer.
        """
        self.canvas.config(bg="white") # Reset canvas background to white for new question
        self.reset_timer() # Reset timer for the new question

        if self.quiz.still_has_questions():
            # Update score display (using current score and question number from quiz brain)
            self.score_label.config(text=f"Score: {self.quiz.score}/{self.quiz.question_number}")

            # Get the current question text and display it on the canvas
            current_q = self.quiz.question_list[self.quiz.question_number]
            q_text = current_q.question_text
            self.canvas.itemconfig(self.question_text, text=q_text, fill=THEME_COLOR) # Set text and its color

            # Re-enable buttons (in case they were disabled after previous answer/timeout)
            self.true_button.config(state="normal")
            self.false_button.config(state="normal")

            self.start_timer() # Start timer for the new question
        else:
            # Quiz has ended
            final_score_message = (
                f"You've completed the quiz!\n"
                f"Your final score: {self.quiz.score}/{len(self.quiz.question_list)}"
            )
            self.canvas.itemconfig(self.question_text, text=final_score_message, fill="black") # Ensure text is visible
            self.true_button.config(state="disabled") # Disable buttons once quiz is over
            self.false_button.config(state="disabled")
            self.stop_timer() # Stop the timer
            messagebox.showinfo("Quiz Finished", final_score_message) # Show a pop-up summary
            # Optionally, close the window after the message box is dismissed:
            # self.window.destroy()

    def check_answer(self, user_choice):
        """
        Handles the user's answer submission.
        Stops the timer, provides feedback, and advances the quiz.
        """
        self.stop_timer() # Stop the timer as soon as an answer is given

        # Disable buttons temporarily to prevent multiple clicks during feedback
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")

        # Get the correct answer for the current question
        current_question = self.quiz.question_list[self.quiz.question_number]
        correct_answer = current_question.correct_answer

        # Check the user's answer using the quiz_brain method
        is_correct = self.quiz.check_answer(user_choice, correct_answer)
        self.give_feedback(is_correct) # Provide visual feedback

        # Advance the quiz brain's question number *after* checking the answer
        self.quiz.next_question()

        # After the feedback delay, load the next question in the UI
        self.window.after(FEEDBACK_DELAY_MS, self.get_next_question)

    def give_feedback(self, is_correct):
        """
        Changes the canvas background color to indicate if the answer was correct or incorrect.
        """
        if is_correct:
            self.canvas.config(bg=CORRECT_COLOR) # Green for correct
        else:
            self.canvas.config(bg=WRONG_COLOR) # Red for wrong

    def start_timer(self):
        """
        Starts or restarts the countdown timer for the current question.
        """
        if self.timer_id: # Cancel any existing timer if one is running
            self.window.after_cancel(self.timer_id)
        self.current_time_left = self.timer_duration
        self.update_timer() # Immediately update to show full time

    def update_timer(self):
        """
        Updates the timer display every second. If time runs out, it marks the answer incorrect.
        """
        if self.current_time_left > 0:
            self.timer_label.config(text=f"Time: {self.current_time_left}s")
            self.current_time_left -= 1
            # Schedule this method to run again after 1 second (1000 milliseconds)
            self.timer_id = self.window.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time: 0s")
            self.stop_timer() # Stop the timer

            # Mark answer as incorrect if time runs out
            self.give_feedback(False)

            # Disable buttons when time runs out to prevent input after feedback
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

            # Advance the quiz brain's question number
            self.quiz.next_question()

            # Wait for feedback delay, then load the next question
            self.window.after(FEEDBACK_DELAY_MS, self.get_next_question)

    def reset_timer(self):
        """
        Resets the timer display and cancels any active timer for a new question.
        """
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
        self.current_time_left = self.timer_duration # Reset time counter
        self.timer_label.config(text=f"Time: {self.timer_duration}s") # Update label
        self.timer_id = None # Clear timer ID

    def stop_timer(self):
        """
        Stops the currently running timer by canceling its scheduled execution.
        """
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None