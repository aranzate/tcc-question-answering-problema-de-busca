import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from ssl import create_default_context # TODO: verificar pq disso
from pprint import pprint

load_dotenv()

class Search:

    # Inicializa o cliente do ElasticSearch
    def __init__(self):
        ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
        ELASTICSEARCH_PORT = os.getenv("ELASTICSEARCH_PORT")
        ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME")
        ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")

        create_default_context()
        self.es = Elasticsearch(
            [f"https://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}"],
            basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
            verify_certs=False
        )
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        # pprint(client_info.body)

    # Deleta e cria um novo índice de nome <index>
    def create_index(self, index):
        self.es.indices.delete(index=index, ignore_unavailable=True) 
        self.es.indices.create(index=index) 

    # Insere um documento em um indice e retorna resposta do elastic search
    def insert_document(self, index, body):
        return self.es.index(index=index, body=body) 
    
    # Insere vários documentos no índice de uma vez
    def insert_documents(self, index, documents):
        operations = []
        for document in documents:
            operations.append({'index': {'_index': index}})
            operations.append(document) 
        return self.es.bulk(operations=operations) #insere vários documentos em uma única chamada de api
    
    def search(self, index, **query_args):
        return self.es.search(index=index, **query_args)

    def retrieve_document(self, index, id):
        return self.es.get(index=index, id=id)

