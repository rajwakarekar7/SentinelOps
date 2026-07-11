from datetime import datetime
import os

BASE_DIR = os.path.dirname(__file__)

LOG_DIR = os.path.join(BASE_DIR, "logs")

LOG_FILE = os.path.join(LOG_DIR, "log.txt")


def log(message):

    os.makedirs(LOG_DIR, exist_ok=True)

    current_time = datetime.now().strftime("%H:%M:%S")

    with open(LOG_FILE, "a") as file:

        file.write(f"[{current_time}] {message}\n")