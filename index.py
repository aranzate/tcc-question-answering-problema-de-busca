import json
from datetime import datetime
import time
from benchmark_recorder import *

class Index: 
    # Recebe a instancia do objeto da classe ElasticSearch e o nome do index
    def __init__(self, es, index): 
        self.es = es
        self.index = index

    # Adiciona os documentos, um de cada vez, ao elastic_search
    def index_documents(self, file_path, array_name):

        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        actions_time = []
        for doc_id, body in enumerate(data[array_name], start=1):
            action_time = calculate_execution_time(self.es.insert_document, doc_id, self.index, body, doc_id)
            actions_time.append(action_time)

        data_log = {
            "function_name": self.index_documents.__name__,
            "file_path": file_path,
            "action_name": self.es.insert_document.__name__,
            "actions_time": actions_time
        } 

        with open(f".\\logs\\{self.index_documents.__name__}_{timestamp}.json", 'w', encoding='utf-8') as json_file:
            json.dump(data_log, json_file, indent=4)

        
    # Adiciona os documentos de uma vez, ao elastic_search
    def index_documents_bulk(self, file_path, array_name):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)[array_name]
            
        calculate_function_execution_time(self.es.insert_documents, self.index, data)
        
