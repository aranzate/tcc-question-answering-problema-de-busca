from search import Search
from utils import *
from metrics import *
import urllib3
import json
import consts
import argparse
import sys
urllib3.disable_warnings() 

def main():
    parser = argparse.ArgumentParser(description='Executa uma função específica com base no parâmetro passado.')
    options = "ls - linear_search, lm - linear_msearch, ps - parallel_search."
    parser.add_argument('func', type=str, help='Alias da função a ser executada: ' + options)
    args = parser.parse_args()

    # Inicializa objeto do elastic search
    es = Search()
    nodes = es.nodes_quantity()
    shards = es.shards_quantity(consts.INDEX)

    #Escreva as respostas encontrados no JSON
    queries = find_queries(consts.QUERIES_PATH)
    answers = find_answers(consts.QUERIES_PATH)
    output_answers_path = consts.RESULT_ANSWERS_PATH
    with open(output_answers_path, 'w') as json_file:
        json.dump(answers, json_file, indent=4)

    # Escolhe a função de busca de acordo com os parâmetros passados
    if args.func == 'ls':
        search_function = linear_search
    elif args.func == 'lm':
        search_function = linear_msearch
    elif args.func == 'ps':
        search_function = parallel_search
    else:
        print("Função não reconhecida. As opções são: " + options)
        sys.exit(1)
    print("Executa " + search_function.__name__ + " com " + str(nodes) + " node(s) e " + str(shards) + " shard(s).")
    found_documents = search_function(es, queries, consts.SEARCHED_DOCUMENTS_QUANTITY, shards, nodes)

    # Escreva os documentos encontrados no JSON
    output_file_path = consts.RESULT_FOUND_PATH
    with open(output_file_path, 'w') as json_file:
        json.dump(found_documents, json_file, indent=4)

    # Carrega dados obtidos dos JSON para calcular precision@k e recall@k
    with open(consts.RESULT_FOUND_PATH, 'r') as found_file:
        found_documents = json.load(found_file)
    with open(consts.RESULT_ANSWERS_PATH, 'r') as answers_file:
        answers = json.load(answers_file)
    precision_at_k(found_documents, answers, 10)
    recall_at_k(found_documents, answers, 10)

if __name__ == '__main__':
    main()