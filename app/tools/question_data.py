import os

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QUESTIONS_NAME = "../data/questions.yml"
QUESTIONS = yaml.safe_load(
    open(os.path.join(BASE_DIR, QUESTIONS_NAME))
)  # load in configuration data


def get_question_number(question_text):
    """Gets the question number from the questions yaml file"""
    for question_number in QUESTIONS["questions"]:
        if QUESTIONS["questions"][question_number] == question_text:
            return question_number
