from search import Search
from index import Index
from utils import *
from metrics import *
import urllib3
import consts
import argparse
import sys
urllib3.disable_warnings() 

def main():
    parser = argparse.ArgumentParser(description='Executa uma função específica com base no parâmetro passado.')
    options = "id - index_documents, ib - index_documents_bulk"
    parser.add_argument('func', type=str, help='Alias da função a ser executada: ' + options)
    args = parser.parse_args()

    # cria index
    es = Search()
    index = Index(es, consts.INDEX)
    es.create_index(consts.INDEX, consts.SHARDS)
    nodes = es.nodes_quantity()
    shards = es.shards_quantity(consts.INDEX)

    # executa indexação de acordo com parâmetros
    if args.func == 'id':
        index_function = index.index_documents
    elif args.func == 'ib':
        index_function = index.index_documents_bulk
    else:
        print("Função não reconhecida. As opções são: " + options)
        sys.exit(1)
    
    print("INDEXACAO: Executa " + index_function.__name__ + " com " + str(nodes) + " node(s) e " + str(shards) + " shard(s).")
    index_function(consts.FILE_PATH, consts.ARRAY_NAME, shards, nodes)

if __name__ == '__main__':
    main()

