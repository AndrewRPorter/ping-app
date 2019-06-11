from datetime import datetime, time

from pytz import timezone

tz = timezone("US/Eastern")


def time_between(begin_time, end_time):
    check_time = datetime.now(tz).time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def get_time_interval():
    if time_between(time(9, 0), time(13, 0)):
        return "T1"
    elif time_between(time(13, 0), time(17, 0)):
        return "T2"
    elif time_between(time(17, 0), time(21, 0)):
        return "T3"
    else:
        return None
