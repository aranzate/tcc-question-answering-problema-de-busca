import json
import urllib3
from search import Search

# desabilita avisos
urllib3.disable_warnings() 

# Inicializa variáveis globais
INDEX = "contextos"
FILE_PATH = ".\\squad-v1.1-pt-master\\contexts.json" 
ARRAY_NAME = 'contexts'

# Cria objeto de busca no elastic search
es = Search()

# Deleta e cria o índice de nome <INDEX>
def delete_and_create_contexts():
    es.create_index(INDEX)

'''
Recebe o caminho para um arquivo json da seguinte estrutura:
{ array: [{ id, any_field1, any_field2 }] }
e adiciona os documentos, um de cada vez, ao elastic_search
'''
def index_documents(file_path, index, array_name):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

        for body in data[array_name]:
            response = es.insert_document(index, body)
            print(f"Objeto indexado: {response['result']}")

'''
Recebe o caminho para um arquivo json da seguinte estrutura:
{ array: [{ id, any_field1, any_field2 }] }
e adiciona os documentos, de uma vez, ao elastic_search
'''
def index_documents_bulk(file_path, index, array_name):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)[array_name]
        es.insert_documents(index, data)


delete_and_create_contexts()
# index_documents(FILE_PATH,  INDEX, ARRAY_NAME)
index_documents_bulk(FILE_PATH,  INDEX, ARRAY_NAME)
