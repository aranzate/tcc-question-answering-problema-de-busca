import time
from datetime import datetime

def calculate_function_execution_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Registra as informações em um arquivo
    with open(f".\\logs\\{func.__name__}_{timestamp}.txt", "a") as log_file:
        log_file.write(f"Função '{func.__name__}' executada em {execution_time:.6f} segundos.\n")

    return result

def calculate_action_execution_time(action, action_name, func_name, timestamp, *args, **kwargs):
    start_time = time.time()
    result = action(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Registra as informações em um arquivo
    with open(f".\\logs\\{func_name}_{timestamp}.txt", "a") as log_file:
        log_file.write(f"Ação '{action_name}' executada em {execution_time:.6f} segundos.\n")

    return result
