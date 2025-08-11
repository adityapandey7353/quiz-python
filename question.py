class Question:
    def __init__(self, question_text, options, correct_answer):
        self.question_text = question_text
        self.options = options  # A list of strings, e.g., ["True", "False"]
        self.correct_answer = correct_answer

    def check_answer(self, user_answer):
        """
        Checks if the user's answer is correct (case-insensitive).
        """
        return user_answer.lower() == self.correct_answer.lower()

    def display_question(self):
        """
        (Used for console testing, not directly by GUI)
        Prints the question and its options.
        """
        print(self.question_text)
        for i, option in enumerate(self.options):
            print(f"{chr(65 + i)}. {option}") # A, B, C, D...
        print("-" * 30) # Separator for readability