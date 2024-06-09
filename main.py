import subprocess
import time

def call(file_name, function):
    command = ["python3", file_name, function]
    result = subprocess.run(command, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")

if __name__ == "__main__":
    call("indexing.py", "ib")
    time.sleep(10)
    call("searching.py", "ls")
    time.sleep(5)
    call("searching.py", "lm")
    time.sleep(5)
    call("searching.py", "ps")
    time.sleep(5)
    call("compare.py", "")
