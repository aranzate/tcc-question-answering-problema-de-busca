import os
import json
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from ssl import create_default_context # TODO: verificar pq disso
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

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
    def insert_document(self, index, body, id):
        return self.es.index(index=index, body=body, id=id) 
    
    # Insere vários documentos no índice de uma vez
    def insert_documents(self, index, documents):
        operations = []
        for document in documents:
            operations.append({'index': {'_index': index}})
            operations.append(document) 
        return self.es.bulk(operations=operations) #insere vários documentos em uma única chamada de api
    
    def find_queries(self, queries_file):
        with open(queries_file, 'r') as file:
            data = json.load(file)
            queries = data['questions']
        return queries
    
    def find_answers(self, queries_file):
        mapping = {}

        with open(queries_file, 'r') as file:
            data = json.load(file)
            questions = data['questions']

            for question in questions:
                question_id = str(question['id_question'])
                context_id = str(question['id_context'])

                if question_id not in mapping:
                    mapping[question_id] = []

                mapping[question_id].append(context_id)

        return mapping

    def linear_search(self, queries, quantity):
        found_documents = {query.get('id_question'): [] for query in queries}

        for query in queries:
            id = query['id_question']
            question = query['question']

            query_busca = {
                "size": quantity,
                "query": {
                    "match": {
                        "context": question  # Busca apenas no contexto específico
                    }
                }
            }
            results = self.search(index="contextos", body=query_busca)

            found_documents[id].extend(hit['_id'] for hit in results['hits']['hits'])

        return found_documents
    
    def precision_at_k(self, documentos_encontrados, documentos_relevantes, k_maximo):
        k_valores = range(1, k_maximo + 1)
        precisao_valores = []
        desvio_padrao_valores = []

        for k in k_valores:
            precisoes = []
            for id, relevant_docs in documentos_relevantes.items():
                documentos_encontrados_query = documentos_encontrados.get(id, [])
                k_documentos_encontrados = documentos_encontrados_query[:k]
                k_relevantes = [doc for doc in k_documentos_encontrados if doc in relevant_docs]
                precisao = len(k_relevantes) / k if k != 0 else 0
                precisoes.append(precisao)

            media_aritmetica_k = np.mean(precisoes)
            desvio_padrao_k = np.std(precisoes)
            
            precisao_valores.append(media_aritmetica_k)
            desvio_padrao_valores.append(desvio_padrao_k)

        # Plot do gráfico
        plt.figure(figsize=(8, 6))
        plt.errorbar(k_valores, precisao_valores, yerr=desvio_padrao_valores, fmt='o-', ecolor='r', capsize=5)
        plt.xlabel('k')
        plt.ylabel('Precision@k (Média)')
        plt.title('Precision@k Gráfico')
        plt.grid(True)
        plt.xticks(k_valores)
        plt.show()


    def recall_at_k(self, documentos_encontrados, documentos_relevantes, k_maximo):
        k_valores = range(1, k_maximo + 1)
        recall_valores = []
        desvio_padrao_valores = []

        for k in k_valores:
            recalls = []
            for query_id, documentos in documentos_relevantes.items():
                documentos_encontrados_query = documentos_encontrados.get(query_id, [])
                documentos_encontrados_k = documentos_encontrados_query[:k]
                documentos_relevantes_set = set(documentos)
                relevante_k = [doc for doc in documentos_encontrados_k if doc in documentos_relevantes_set]
                recall = len(relevante_k) / len(documentos) if len(documentos) != 0 else 0
                recalls.append(recall)
            
            media_recall_k = np.mean(recalls)
            desvio_padrao_recall_k = np.std(recalls)
            recall_valores.append(media_recall_k)
            desvio_padrao_valores.append(desvio_padrao_recall_k)

        # Plot do gráfico
        plt.figure(figsize=(8, 6))
        plt.errorbar(k_valores, recall_valores, yerr=desvio_padrao_valores, fmt='o-', ecolor='r', capsize=5)
        plt.xlabel('k')
        plt.ylabel('Recall@k (Média)')
        plt.title('Recall@k Gráfico')
        plt.grid(True)
        plt.xticks(k_valores)
        plt.show()

    def search(self, index, **query_args):
        return self.es.search(index=index, **query_args)
    
    def msearch(self, index, **query_args):
        return self.es.msearch(index=index, **query_args)

    def retrieve_document(self, index, id):
        return self.es.get(index=index, id=id)

