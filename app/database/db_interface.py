import os
import random
import time

import pyrebase
import xxhash
import yaml

from ..models.user import User
from ..tools import question_data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# change CONFIG file location based on where the program is being run
CONFIG_NAME = "../config.yml"
CONFIG = yaml.safe_load(
    open(os.path.join(BASE_DIR, CONFIG_NAME))
)  # load in configuration data

firebase_conf = {
    "apiKey": CONFIG["firebase"]["API_KEY"],
    "authDomain": CONFIG["firebase"]["AUTH_DOMAIN"],
    "databaseURL": CONFIG["firebase"]["DATABASE_URL"],
    "projectId": CONFIG["firebase"]["PROJECT_ID"],
    "storageBucket": CONFIG["firebase"]["STORAGE_BUCKET"],
    "messagingSenderId": CONFIG["firebase"]["SENDER_ID"],
}

firebase = pyrebase.initialize_app(firebase_conf)
db = firebase.database()


class DBInterface:
    @classmethod
    def create_user(cls, data):
        """Creates new user model from initial CSV data"""

        data = {
            "firstName": data["firstName"],
            "lastName": data["lastName"],
            "phoneNumber": data["phoneNumber"],
            "userID": data["userID"],
            "lastQuestion": "",
            "lastQuestionTime": 0,
            "cycleA": False,
            "cycleB": False,
            "lastCycleTime": time.time(),
            "nextCycleTime": random.randint(0, 240) * 60,
            "startTime": time.time(),
            "lastIntervalTime": 0,
            "currentInterval": "T1",
            "isPaused": False,
            "waiting": False,
            "finished": False,
            "reset": False,
            "stop": False
        }

        hash_id = xxhash.xxh64(data["userID"], seed=27).hexdigest()

        user_obj = User(hash_id, data)

        # check if user already exists
        if user_obj.phone_number in [
            user.phone_number for user in DBInterface.get_all_users()
        ]:
            return {"user": DBInterface.get_user(user_obj.phone_number)}

        db.child("participants").child(hash_id).set(data)

        return {"user": user_obj}

    @classmethod
    def update_user(cls, user):
        """Updates user information in firebase"""
        hash_id = xxhash.xxh64(user.id, seed=27).hexdigest()
        user_data = user.to_dict()
        db.child("participants").child(hash_id).set(user_data)

    @classmethod
    def add_response(cls, user, question, response, timestamp, stop=False):
        """Updates responses in firebase"""
        hash_id = xxhash.xxh64(user.id, seed=27).hexdigest()

        try:
            data = dict(db.child("responses").child(hash_id).get().val())
        except TypeError:
            data = {}

        question_number = question_data.get_question_number(question)
        current_time = time.time()

        day = (
            int((current_time - user.start_time) / 86400) + 1
        )  # note that 86400 is seconds in a day

        time_interval = user.current_interval

        if not user.cycleB:
            data[f"D{day}_{time_interval}_A_{question_number}"] = {
                "response": response,
                "questionTimestamp": user.last_question_time,
                "responseTimestamp": timestamp,
                "stop": stop
            }
        else:
            data[f"D{day}_{time_interval}_B_{question_number}"] = {
                "response": response,
                "questionTimestamp": user.last_question_time,
                "responseTimestamp": timestamp,
                "stop": stop
            }

        db.child("responses").child(hash_id).set(data)

    @classmethod
    def get_user(cls, number):
        """Returns user object from database by matching phone numbers"""

        all_users = DBInterface.get_all_users()

        for user in all_users:
            if user.phone_number == number:
                return user

        return None

    @classmethod
    def get_all_users(cls):
        """Returns all user objects from the database in a list"""
        try:
            all_user_data = dict(db.child("participants").get().val())
        except TypeError:
            return {}

        return [User(key, value) for key, value in all_user_data.items()]

    @classmethod
    def get_user_responses(cls, key):
        """Query specific user responses"""
        all_data = DBInterface.get_all_responses()

        if key in all_data:
            return all_data[key]
        return {}

    @classmethod
    def get_all_responses(cls):
        """Query all responses from the table"""
        try:
            all_response_data = dict(db.child("responses").get().val())
        except TypeError:
            return {}

        return all_response_data
