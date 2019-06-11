import argparse
import os

from plan import Plan

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_NAME = "ping-app/start_cron.py"
SCRIPT_NAME_PATH = os.path.join(BASE_DIR, SCRIPT_NAME)

cron = Plan()

cron.command(f"python3 {SCRIPT_NAME_PATH} --start", every="1.day", at="hour.9 minute.0")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", action="store_true")
    parser.add_argument("-e", "--end", action="store_true")
    args = parser.parse_args()

    if args.start:
        cron.run("write")
    elif args.end:
        cron.run("clear")
    else:
        cron.run("clear")
