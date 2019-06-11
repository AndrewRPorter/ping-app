import argparse
import os

from plan import Plan

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_NAME = "ping-app/cron.py"
SCRIPT_NAME_PATH = os.path.join(BASE_DIR, SCRIPT_NAME)

cron = Plan()

cron.command(f"python3 {SCRIPT_NAME_PATH}", every="1.minute")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", action="store_true")
    parser.add_argument("-e", "--end", action="store_true")
    args = parser.parse_args()

    if args.start:
        os.system(
            f"python3 {SCRIPT_NAME_PATH}"
        )  # call the command first and then call every 1.minutes
        cron.run("write")
    elif args.end:
        cron.run("clear")
    else:
        cron.run("clear")
