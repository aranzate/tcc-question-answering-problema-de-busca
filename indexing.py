from search import Search
from index import Index
from utils import *
from metrics import *
import urllib3
import consts
import argparse
urllib3.disable_warnings() 

def main():
    parser = argparse.ArgumentParser(description='Executa uma função específica com base no parâmetro passado.')
    options = "id - index_documents, ib - index_documents_bulk"
    parser.add_argument('func', type=str, help='Alias da função a ser executada: ' + options)
    args = parser.parse_args()

    es = Search()
    index = Index(es, consts.INDEX)
    nodes = es.nodes_quantity()
    shards = es.shards_quantity(consts.INDEX)

    es.create_index(consts.INDEX, shards)

    if args.func == 'id':
        index.index_documents(consts.FILE_PATH, consts.ARRAY_NAME, shards, nodes)
    elif args.func == 'ib':
        index.index_documents_bulk(consts.FILE_PATH, consts.ARRAY_NAME, shards, nodes)
    else:
        print("Função não reconhecida. As opções são: " + options)

if __name__ == '__main__':
    main()

