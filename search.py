import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from ssl import create_default_context 
from pprint import pprint
import warnings

load_dotenv()

'''
Classe para inicialização do cliente do ElasticSearch 
com os métodos que interagem com o servidor do ElasticSearch
'''

class Search:

    # Inicializa o cliente do ElasticSearch
    def __init__(self):
        ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
        ELASTICSEARCH_PORT = os.getenv("ELASTICSEARCH_PORT")
        ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME")
        ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")

        create_default_context()
        warnings.filterwarnings("ignore")

        self.es = Elasticsearch(
            [f"https://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}"],
            basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
            verify_certs=False
        )
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        # pprint(client_info.body)

    # Deleta e cria um novo índice de nome <index>
    def create_index(self, index, shards):
        self.es.indices.delete(index=index, ignore_unavailable=True) 
        self.es.indices.create(index=index, body={
                                   'settings': {
                                       'index': {
                                           'number_of_shards': shards,
                                           #'number_of_replicas': 0
                                       }
                                   }
                               })
        

    # Insere um documento em um indice e retorna resposta do elastic search
    def insert_document(self, index, body, id):
        return self.es.index(index=index, body=body, id=id) 
    
    # Insere vários documentos no índice de uma vez
    def insert_documents(self, index, documents):
        operations = []
        for document in documents:
            operations.append({'index': {'_index': index, '_id': document['context_id']}})
            operations.append(document) 
        return self.es.bulk(operations=operations) #insere vários documentos em uma única chamada de api

    def search(self, index, **query_args):
        return self.es.search(index=index, **query_args)
    
    def msearch(self, index, **query_args):
        return self.es.msearch(index=index, request_timeout=1000 ,max_concurrent_shard_requests=5, max_concurrent_searches=5, **query_args)

    def retrieve_document(self, index, id):
        return self.es.get(index=index, id=id)
    
    def nodes_quantity(self):
        return self.es.nodes.stats()["_nodes"]["total"]
    
    def shards_quantity(self, index):
        result = self.es.indices.get(index=index)[index]["settings"]["index"]["number_of_shards"]
        return int(result)
    
    def close(self):
        self.es.close()
        print("Elasticsearch connection closed.\n")

