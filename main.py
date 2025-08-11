# main.py (modified)
from question import Question
from quiz_brain import QuizBrain
# from questions_data import question_data # No longer needed if using API
from ui import QuizInterface
from api_manager import TriviaAPI # <-- Import our new API manager
import html # To decode HTML entities in questions

# 1. Fetch questions from the API
# You can configure the number of questions and type here
api = TriviaAPI(amount=10, question_type="boolean") # For True/False questions
api_question_data = api.get_questions()

if not api_question_data:
    print("Failed to load questions from API. Exiting.")
    exit() # Or load from local questions_data.py as a fallback

# 2. Prepare the question bank from API data
question_bank = []
for item in api_question_data:
    # Decode HTML entities for question text and answers
    q_text = html.unescape(item["question"])
    q_answer = html.unescape(item["correct_answer"])

    # Open Trivia DB returns "True" or "False" strings, which aligns with our current logic
    # For 'multiple' choice, 'incorrect_answers' is a list.
    # Our current Question class and UI expects simple True/False options.
    # If you switch to 'multiple' type, you'll need to update Question and UI accordingly.
    q_options = ["True", "False"] # Fixed options for boolean questions from API

    new_question = Question(q_text, q_options, q_answer)
    question_bank.append(new_question)

# 3. Initialize the QuizBrain
quiz = QuizBrain(question_bank)

# 4. Initialize the GUI
quiz_ui = QuizInterface(quiz)