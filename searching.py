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
    parser.add_argument('folder_name', nargs="?", default="", help='Nome da pasta')
    args = parser.parse_args()

    # Inicializa objeto do elastic search
    es = Search()
    nodes = es.nodes_quantity()
    shards = es.shards_quantity(consts.INDEX)

    #Escreva as respostas encontrados no JSON
    queries = find_queries(consts.QUERIES_PATH)

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
    
    print("BUSCA: Executa " + search_function.__name__ + " com " + str(nodes) + " node(s) e " + str(shards) + " shard(s).")
    search_function(es, queries, consts.SEARCHED_DOCUMENTS_QUANTITY, shards, nodes, args.folder_name)

if __name__ == '__main__':
    main()