import time

def save_feedback(message: str):
    time.sleep(5)

    with open("feedback.txt", "a") as file:
        file.write(message + "\n")