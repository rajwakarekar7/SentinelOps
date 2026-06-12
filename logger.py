from datetime import datetime

def log(message):

    file = open("log.txt" , "a")

    current_time = datetime.now().strftime("%H:%M:%S")

    file.write(f"[{current_time}] {message}\n")

    file.close()