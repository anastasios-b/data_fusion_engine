import os
import datetime

# Functions used for logging messages and results to files
def log_message(message):
    os.makedirs("./logs", exist_ok=True)
    with open("./logs/info.log", "a") as log_file:
        log_file.write("[INFO {}] {}\n".format(datetime.datetime.now(), message))

def log_result(result):
    os.makedirs("./logs", exist_ok=True)
    with open("./logs/results.log", "a") as result_file:
        result_text = "[Result {}] {}\n".format(datetime.datetime.now(), str(result))
        result_file.write(result_text)