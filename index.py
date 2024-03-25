import json
from datetime import datetime
import time
from benchmark_recorder import calculate_action_execution_time

class Index: 
    # Recebe a instancia do objeto da classe ElasticSearch e o nome do index
    def __init__(self, es, index): 
        self.es = es
        self.index = index

    '''
    Recebe o caminho para um arquivo json da seguinte estrutura:
    { array: [{ id, any_field1, any_field2 }] }
    e adiciona os documentos, um de cada vez, ao elastic_search
    '''
    def index_documents(self, file_path, array_name):
        def action(body):
            self.es.insert_document(self.index, body)

        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f".\\logs\\{self.index_documents.__name__}_{timestamp}.txt", 'w', encoding='utf-8') as file:
            file.write(f"Função {self.index_documents.__name__} no arquivo {file_path}\n")
        
        for body in data[array_name]:
            calculate_action_execution_time(action, "Objeto indexado", self.index_documents.__name__, timestamp, body)
        
    '''
    Recebe o caminho para um arquivo json da seguinte estrutura:
    { array: [{ id, any_field1, any_field2 }] }
    e adiciona os documentos, de uma vez, ao elastic_search
    '''
    def index_documents_bulk(self, file_path, array_name):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)[array_name]
        self.es.insert_documents(self.index, data)
