import time
from datetime import datetime
import json

# Calcula o tempo de execução de uma função e salva em um arquivo 
def calculate_function_execution_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Registra as informações em um arquivo
    with open(f".\\logs\\{func.__name__}_{timestamp}.txt", "a", encoding='utf-8') as log_file:
        log_file.write(f"Função '{func.__name__}' executada em {execution_time:.6f} segundos.\n")

    return result

# escreve um log json
def write_log(function_name, origin, action_name, actions, timestamp):
    data_log = {
        "function_name": function_name,
        "origin": origin,
        "action_name": action_name,
        "actions": actions
    } 

    with open(f".\\logs\\{function_name}_{timestamp}.json", 'w', encoding='utf-8') as json_file:
        json.dump(data_log, json_file, indent=4)

# Executa uma função e retorna o id, o tempo e o retorno da função 
def calculate_execution_time(func, id, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return {"id": id, "time":  execution_time}, result

