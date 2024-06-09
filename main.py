import subprocess
import time
import os
from datetime import datetime
import consts
from search import Search

def call(file_name, *args):
    command = ["python3", file_name] + list(args)
    result = subprocess.run(command, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")

if __name__ == "__main__":
    # obtém nodes
    es = Search()
    print("Buscando quantidade de nós.")
    nodes = str(es.nodes_quantity())
    es.close()

    # obtém shards 
    shards = str(consts.SHARDS)

    # cria pasta 
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f'.{consts.SEPARATOR_PATH}{consts.LOGS_PATH}{nodes}_nodes_{shards}_shards_{timestamp}'
    os.makedirs(folder_name)
    folder_name += consts.SEPARATOR_PATH

    # chama arquivos
    call("indexing.py", "ib", shards, folder_name)
    time.sleep(10)
    call("searching.py", "ls", folder_name)
    time.sleep(5)
    call("searching.py", "lm", folder_name)
    time.sleep(5)
    call("searching.py", "ps", folder_name)
    time.sleep(5)
    call("compare.py", nodes, shards, folder_name)

    print("Finalizado. Você pode encontrar os logs na pasta: " + folder_name + "./n/n")
