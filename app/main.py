import random
import time
from datetime import datetime

from flask import Flask, request
from pytz import timezone

from app.database.db_interface import DBInterface as db
from cron import get_next_question, send_message

_participant_file = "./data/participants.csv"

tz = timezone("US/Eastern")  # setting EST timezone information


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        """
        Landing page for testing server connection
        """
        return "ping-app landing page..."

    @app.route("/sms", methods=["POST"])
    def sms():
        """
        Exposes SMS endpoint to receive message reply data and handles the communications
        with the database
        """
        number = request.form["From"]
        message_body = request.form["Body"]
        timestamp = str(datetime.now(tz))
        user = db.get_user(number)

        if user is None:  # prevent against double responses
            return ""

        if user.finished:
            return ""

        response_question = user.last_question  # question that participant was asked
        question = get_next_question(response_question)

        db.add_response(user, response_question, message_body, timestamp)

        if question != "done":
            user.last_question = question
            user.last_question_time = timestamp
            db.update_user(user)
            send_message(user, question)
        else:
            user.waiting = False
            user.last_cycle_time = time.time()
            user.next_cycle_time = random.randint(8, 12) * 60

            if user.cycleA and user.cycleB:
                user.next_cycle_time = random.randint(0, 240) * 60
                user.last_interval_time = time.time()
                user.is_paused = True

        db.update_user(user)

        return ""

    return app


application = create_app()
