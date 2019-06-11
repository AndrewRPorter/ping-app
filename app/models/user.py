class User:
    def __init__(self, key, data):
        self.key = key
        self.first_name = data["firstName"]
        self.last_name = data["lastName"]
        self.phone_number = data["phoneNumber"]
        self.id = data["userID"]
        self.last_question = data["lastQuestion"]
        self.last_question_time = data["lastQuestionTime"]
        self.last_cycle_time = data["lastCycleTime"]
        self.cycleA = data["cycleA"]
        self.cycleB = data["cycleB"]
        self.next_cycle_time = data["nextCycleTime"]
        self.start_time = data["startTime"]
        self.last_interval_time = data["lastIntervalTime"]
        self.current_interval = data["currentInterval"]
        self.is_paused = data["isPaused"]
        self.waiting = data["waiting"]
        self.finished = data["finished"]
        self.reset = data["reset"]

    def to_dict(self):
        """Returns a dictionary representation of user data for easy storage"""
        return {
            "userID": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "phoneNumber": self.phone_number,
            "lastQuestion": self.last_question,
            "lastQuestionTime": self.last_question_time,
            "lastCycleTime": self.last_cycle_time,
            "cycleA": self.cycleA,
            "cycleB": self.cycleB,
            "nextCycleTime": self.next_cycle_time,
            "startTime": self.start_time,
            "lastIntervalTime": self.last_interval_time,
            "currentInterval": self.current_interval,
            "isPaused": self.is_paused,
            "waiting": self.waiting,
            "finished": self.finished,
            "reset": self.reset,
        }

    def __repr__(self):
        return str(f"{self.first_name} {self.last_name}")

    def __str__(self):
        return str(self.first_name)
