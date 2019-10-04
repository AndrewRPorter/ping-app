import csv
import os
import random
import time
from datetime import datetime

import yaml
from pytz import timezone
from twilio.rest import Client

from app.database.db_interface import DBInterface as db
from app.tools import time_helper

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_NAME = "ping-app/config.yml"
CONFIG = yaml.safe_load(
    open(os.path.join(BASE_DIR, CONFIG_NAME))
)  # load in configuration data

QUESTIONS_NAME = "ping-app/data/questions.yml"
QUESTIONS = yaml.safe_load(
    open(os.path.join(BASE_DIR, QUESTIONS_NAME))
)  # load in configuration data

account_sid = CONFIG["twilio"]["ACCOUNT_SID"]
auth_token = CONFIG["twilio"]["AUTH_TOKEN"]

_participant_file = os.path.join(BASE_DIR, "ping-app/data/participants.csv")

tz = timezone("US/Eastern")  # setting EST timezone information

client = Client(account_sid, auth_token)


def initialize():
    # create participant CSV if not already exists
    if not os.path.isfile(_participant_file):
        with open(_participant_file, "w") as f:
            writer = csv.writer(
                f, delimiter=",", quotechar="'", quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(["ID", "First Name", "Last Name", "Number"])

    # from here we want to add all users to the firebase table if not already in there
    with open(_participant_file, "r") as f:
        reader = csv.reader(f, delimiter=",", quotechar="'", quoting=csv.QUOTE_MINIMAL)

        i = 0  # used to track when CSV column headers are found

        for row in reader:
            if i == 0:
                i += 1
                continue  # skip over column names

            data = {
                "userID": row[0],
                "firstName": row[1],
                "lastName": row[2],
                "phoneNumber": row[3],
            }
            db.create_user(data)


def send_message(user, question):
    """
    Handles user response messages for each cycle
    """
    client.messages.create(to=user.phone_number, from_=CONFIG["twilio"]["NUMBER"], body=question)


def send_initial_message(user):
    """
    Handles the initial message sending task for a given number

    This is responsbile for starting new user cycles
    """

    if time_helper.get_time_interval() is None:  # if not between 9:00AM and 9:00PM
        return

    current_time = time.time()  # grab current time

    # check to see if a user cycle has begun yet, if not start cycleA
    if not user.cycleA and not user.cycleB:
        if (current_time - user.last_cycle_time) > user.next_cycle_time:
            user.current_interval = (
                time_helper.get_time_interval()
            )  # only update user time intervals in cycleA

            user.waiting = True
            user.cycleA = True  # cycle A has now been started
            question = get_next_question(user.last_question)

            user.last_question = question
            user.last_question_time = str(datetime.now(tz))

            client.messages.create(
                to=user.phone_number, from_="+19783869580", body=question
            )
    elif user.cycleA and not user.cycleB:
        # need to check time since last cycle here (8-12 minutes)

        if not user.next_cycle_time == 0 and (
            (current_time - user.last_cycle_time) > user.next_cycle_time
        ):
            user.waiting = True
            user.cycleB = True  # cycle B has now been started
            question = QUESTIONS["questions"][
                "one"
            ]  # reset last question for current cycle

            user.last_question = question
            user.last_question_time = str(datetime.now(tz))

            client.messages.create(
                to=user.phone_number, from_="+19783869580", body=question
            )

    db.update_user(user)  # send updated user object to the DB


def send_all_messages():
    """
    Send messages to all participants from CSV file
    """

    current_time = time.time()

    for user in db.get_all_users():
        if user.stop:
            continue
        if user.finished:
            continue
        elif user.is_paused:  # if paused see if we can unset the pause
            # check that we are in a new time interval first
            if user.current_interval == time_helper.get_time_interval():
                continue

            # check and see if 5 days have past, this is a hard stop for the time being
            day = (
                int((current_time - user.start_time) / 86400) + 1
            )  # note that 86400 is seconds in a day
            if day == 5 and user.current_interval == "T3" and user.cycleA and user.cycleB:
                user.finished = True
                db.update_user(user)  # send updated user object to the DB
                continue

            # don't send user messages if already finished last cycle
            # wait for transition to next day
            if user.current_interval == "T3":
                user.reset = True
                db.update_user(user)
                if time_helper.get_time_interval() == "T1":
                    user.current_interval = time_helper.get_time_interval()
                    user.is_paused = False
                    user.last_question = (
                        ""
                    )  # reset the last question asked to create a new cycle of questions
                    # user.last_cycle_time = current_time  # reset the cycle clock
                    user.cycleA, user.cycleB = (
                        False,
                        False,
                    )  # reset both cycles for new time
                    user.next_cycle_time = random.randint(0, 240) * 60
                    user.last_cycle_time = time.time()
                    db.update_user(user)
                continue

            if (
                current_time - user.last_interval_time
            ) > 7200:  # check that AT LEAST 2 hours has passed by
                user.is_paused = False
                user.last_question = (
                    ""
                )  # reset the last question asked to create a new cycle of questions
                user.last_cycle_time = time.time()
                user.next_cycle_time = random.randint(0, 240) * 60

                if (
                    user.next_cycle_time + 7200
                ) > 14400:  # if more than 4 hours have passed
                    user.next_cycle_time = random.randint(0, 120) * 60

                # user.last_cycle_time = current_time  # reset the cycle clock
                user.cycleA, user.cycleB = (
                    False,
                    False,
                )  # reset both cycles for new time points
                db.update_user(user)  # send updated user object to the DB
        else:
            # if user is not currently in a cycle, initiate a new one
            if not user.waiting:
                day = int((current_time - user.start_time) / 86400) + 1
                if day > 1 and user.reset is True:
                    user.reset = False
                    user.next_cycle_time = random.randint(0, 240) * 60
                    db.update_user(user)
                send_initial_message(user)


def get_next_question(last_question):
    """
    Returns the next question from the yaml file, givent he last asked question
    """
    question = ""

    if last_question == "":
        question = QUESTIONS["questions"]["one"]
    elif last_question == QUESTIONS["questions"]["one"]:
        question = QUESTIONS["questions"]["two"]
    elif last_question == QUESTIONS["questions"]["two"]:
        question = QUESTIONS["questions"]["three"]
    elif last_question == QUESTIONS["questions"]["three"]:
        question = QUESTIONS["questions"]["four"]
    else:
        question = "done"  # denotes end of current cycle

    return question


if __name__ == "__main__":
    initialize()  # start the client processes
    send_initial_message(db.get_all_users()[0])
    send_all_messages()
