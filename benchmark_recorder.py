import time
from datetime import datetime
import json
import consts
import statistics

# Escreve um log em formato json 
def write_log(function_name, origin, action_name, actions, timestamp, nodes, shards, time_python_function, folder_name="", mean=True, variance=True, standard_deviation=True):
    
    data_log = {
        "function_name": function_name,
        "origin": origin,
        "action_name": action_name,
        "nodes": nodes,
        "shards": shards,
        "time_python_function": time_python_function
    } 

    time_values = [item["time"] for item in actions]
    if(mean):
        data_log["mean"]=statistics.mean(time_values)
    if(variance):
        data_log["variance"]=statistics.variance(time_values)
    if(standard_deviation):
        data_log["standard_deviation"]=statistics.stdev(time_values)
        
    data_log["actions"]=actions

    if(folder_name == ""): 
        folder_name = f".{consts.SEPARATOR_PATH}{consts.LOGS_PATH}"

    with open(f"{folder_name}n{nodes}_s{shards}_log_{function_name}.json", 'w', encoding='utf-8') as json_file:
        json.dump(data_log, json_file, indent=4)

# Executa uma função e retorna o id, o tempo e o retorno da função 
def calculate_execution_time(func, id, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return {"id": id, "time_python":  execution_time, "time": result.get('took', 0) / 1000}, result

def msearch_execution_time(results, ids):
    execution_times = []
    for id, result in zip(ids, results['responses']):
        execution_times.append({"id": id, "time": result.get('took', 0) / 1000})  # Convertendo de ms para segundos
    return execution_times
