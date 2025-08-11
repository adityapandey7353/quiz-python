import random
from question import Question # Import our Question class

class QuizBrain:
    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.question_list = question_list # List of Question objects
        random.shuffle(self.question_list) # Shuffle questions at the start for variety

    def still_has_questions(self):
        """
        Checks if there are more questions remaining in the quiz.
        """
        return self.question_number < len(self.question_list)

    def next_question(self):
        """
        Advances to the next question in the quiz logic.
        This method increments the question_number,
        but the actual display is handled by the UI.
        """
        if self.still_has_questions():
            self.question_number += 1
            # The UI will call get_next_question() to display it
            # print(f"DEBUG: Next question number: {self.question_number}") # For debugging if needed
        else:
            # All questions asked, quiz is over
            pass # The UI handles the end of quiz message

    def check_answer(self, user_answer, correct_answer):
        """
        Checks the user's answer against the correct one and updates the score.
        Returns True if correct, False otherwise.
        """
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            # print("You got it right!") # Console feedback, now handled by GUI
            return True
        else:
            # print("That's wrong.") # Console feedback, now handled by GUI
            return False
        # print(f"Your current score is: {self.score}/{self.question_number}\n") # Console feedback, now handled by GUI