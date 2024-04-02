import json
from datetime import datetime
import time
from benchmark_recorder import calculate_action_execution_time, calculate_function_execution_time

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
        with open(f".\\logs\\{self.index_documents.__name__}_{timestamp}.txt", 'w', encoding='utf-8') as file:
            file.write(f"Função {self.index_documents.__name__} no arquivo {file_path}\n")

        for doc_id, body in enumerate(data[array_name], start=1):
            # Aqui, doc_id é usado como o ID do documento. Você pode ajustar isso conforme necessário.
            calculate_action_execution_time(self.es.insert_document, self.index_documents.__name__, timestamp, self.index, body, doc_id)
            
    # Adiciona os documentos de uma vez, ao elastic_search
    def index_documents_bulk(self, file_path, array_name):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)[array_name]
            
        calculate_function_execution_time(self.es.insert_documents, self.index, data)
        
