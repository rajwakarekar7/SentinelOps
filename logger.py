from datetime import datetime
import os

LOG_FILE = os.path.join(

    os.path.dirname(__file__),

    "logs",
    "log.txt"
)

def log(message):

    file = open( LOG_FILE , "a")

    current_time = datetime.now().strftime("%H:%M:%S")

    file.write(f"[{current_time}] {message}\n")

    file.close()