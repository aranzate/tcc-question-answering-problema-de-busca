import subprocess
import time
import os
from datetime import datetime
import consts

def call(file_name, function, folder_name):
    command = ["python3", file_name, function, folder_name]
    result = subprocess.run(command, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")

if __name__ == "__main__":
    # cria pasta 
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f'.{consts.SEPARATOR_PATH}{consts.LOGS_PATH}{timestamp}'
    os.makedirs(folder_name)
    folder_name += consts.SEPARATOR_PATH

    call("indexing.py", "ib", folder_name)
    time.sleep(10)
    call("searching.py", "ls", folder_name)
    time.sleep(5)
    call("searching.py", "lm", folder_name)
    time.sleep(5)
    call("searching.py", "ps", folder_name)
    time.sleep(5)
    # call("compare.py", "", folder_name)
