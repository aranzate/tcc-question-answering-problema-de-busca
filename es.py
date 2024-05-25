from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
import time
import concurrent.futures
from ssl import create_default_context
import urllib3
import json
import os
from dotenv import load_dotenv
import consts

urllib3.disable_warnings()

load_dotenv()
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
ELASTICSEARCH_PORT = os.getenv("ELASTICSEARCH_PORT")
ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")

# Initialize Elasticsearch client
ssl_context = create_default_context()
client = Elasticsearch(
    [f"https://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}"],
    basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
    verify_certs=False
)


def indexar_documentos(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)
        tempo_inicio = time.time()

        def indexar_contexto(contexto):
            id_contexto = contexto['context_id']
            resposta = client.index(index="contextos", id=id_contexto, body=contexto)
            print(f"Contexto {id_contexto} indexado: {resposta['result']}")

        for contexto in dados['contexts']:
            indexar_contexto(contexto)

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     executor.map(indexar_contexto, dados['contexts'])    

        tempo_fim = time.time()
        tempo_percorrido = tempo_fim - tempo_inicio
        print(f"Tempo percorrido de indexação: {tempo_percorrido} segundos")

def documentos_relevantes(caminho_arquivo):
    mapeamento = {}

    with open(caminho_arquivo, 'r') as arquivo:
        dados = json.load(arquivo)
        perguntas = dados['questions']

        for pergunta in perguntas:
            question_id = str(pergunta['id_question'])
            context_id = str(pergunta['id_context'])

            if question_id not in mapeamento:
                mapeamento[question_id] = []

            mapeamento[question_id].append(context_id)

    #print(mapeamento)
    return mapeamento

def encontrar_queries(queries_arquivo):
    with open(queries_arquivo, 'r') as arquivo:
        dados = json.load(arquivo)
        queries = dados['questions']
    return queries


def buscar(queries, quantidade):

    documentos_encontrados = {query.get('id_question'): [] for query in queries}

    tempo_inicio = time.time()

    for query in queries:
        id = query['id_question']
        texto_pergunta = query['question']

        query_busca = {
            "size": quantidade,
            "query": {
                "match": {
                    "context": texto_pergunta  # Busca apenas no contexto específico
                }
            }
        }
        

        tempo_inicio_busca = time.time()  

        resultados = client.search(index="contextos", body=query_busca)

        tempo_fim_busca = time.time()
        tempo_busca = tempo_fim_busca - tempo_inicio_busca
        print(f"Busca para a consulta {id} levou {tempo_busca} segundos")

        documentos_encontrados[id].extend(hit['_id'] for hit in resultados['hits']['hits'])

    tempo_fim = time.time()
    tempo_percorrido = tempo_fim - tempo_inicio
    print(f"Tempo percorrido de busca: {tempo_percorrido} segundos")

    return documentos_encontrados

def buscar_paralelo(queries, quantidade):

    documentos_encontrados = {query.get('id_question'): [] for query in queries}

    def buscar_documento(query):
        id = query['id_question']
        texto_pergunta = query['question']

        query_busca = {
            "size":quantidade,
            "query": {
                "match": {
                    "context": texto_pergunta  # Busca apenas no contexto específico
                }
            }
        }

        tempo_inicio_busca = time.time()  

        resultados = client.search(index="contextos", body=query_busca)

        tempo_fim_busca = time.time()
        tempo_busca = tempo_fim_busca - tempo_inicio_busca
        print(f"Busca para a consulta {id} levou {tempo_busca} segundos")

        documentos_encontrados[id].extend(hit['_id'] for hit in resultados['hits']['hits'])

    tempo_inicio = time.time()

    #ThreadPoolExecutor realiza buscas em paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(buscar_documento, queries)

    tempo_fim = time.time()
    tempo_percorrido = tempo_fim - tempo_inicio
    print(f"Tempo percorrido de busca: {tempo_percorrido} segundos")

    return documentos_encontrados


def precision_at_k(documentos_encontrados, documentos_relevantes, k_maximo):
    k_valores = range(1, k_maximo+1)
    precisao_valores = []

    for k in k_valores:
        soma_precisao = 0
        for id, relevant_docs in documentos_relevantes.items():
            documentos_encontrados_query = documentos_encontrados.get(int(id), [])
            k_documentos_encontrados = documentos_encontrados_query[:k]
            documentos_relevantes_set = set(relevant_docs)
            k_relevantes = [doc for doc in k_documentos_encontrados if doc in documentos_relevantes_set]
            precisao = len(k_relevantes) / k if k != 0 else 0
            soma_precisao += precisao
        media_aritmetica_k = soma_precisao / len(documentos_relevantes)
        precisao_valores.append(media_aritmetica_k)

    #Plot do gráfico
    plt.figure(figsize=(8, 6))
    plt.plot(k_valores, precisao_valores, marker='o', linestyle='-')
    plt.xlabel('k')
    plt.ylabel('Precision@k (Média)')
    plt.title('Precision@k Gráfico')
    plt.grid(True)
    plt.xticks(k_valores)
    plt.show()

def recall_at_k(documentos_encontrados, documentos_relevantes, k_maximo):
    k_valores = range(1, k_maximo+1)
    recall_valores = []

    for k in k_valores:
        recall_soma = 0
        for query_id, documentos in documentos_relevantes.items():
            documentos_encontrados_query = documentos_encontrados.get(int(query_id), [])
            documentos_encontrados_k = documentos_encontrados_query[:k]
            documentos_relevantes_set = set(documentos)
            relevante_k = [doc for doc in documentos_encontrados_k if doc in documentos_relevantes_set]
            recall = len(relevante_k) / len(documentos) if len(documentos) != 0 else 0
            recall_soma += recall
        media_recall_k = recall_soma / len(documentos_relevantes)
        recall_valores.append(media_recall_k)

    #Plot do gráfico
    plt.figure(figsize=(8, 6))
    plt.plot(k_valores, recall_valores, marker='o', linestyle='-')
    plt.xlabel('k')
    plt.ylabel('Recall@k (Média)')
    plt.title('Recall@k Gráfico')
    plt.grid(True)
    plt.xticks(k_valores)
    plt.show()

indexar_documentos(consts.FILE_PATH)
queries = encontrar_queries(consts.QUERIES_PATH)
gabarito = documentos_relevantes(consts.QUERIES_PATH)
documentos_encontrados = buscar(queries, 5)
precision_at_k(documentos_encontrados, gabarito, 5)
recall_at_k(documentos_encontrados, gabarito, 5)
