from search import Search
from index import Index
from utils import *
from metrics import *
import urllib3
import json

# desabilita avisos
urllib3.disable_warnings() 

# Inicializa variáveis globais
INDEX = "contextos"
FILE_PATH = ".\\ignorar\\contexts.json" # ".\\squad-v1.1-pt-master\\contexts.json"
QUERIES_PATH = ".\\ignorar\\questions.json" # ".\\squad-v1.1-pt-master\\questions.json"
ARRAY_NAME = 'contexts'
SEARCHED_DOCUMENTS_QUANTITY = 10

# Cria objeto de busca no elastic search
es = Search()

# Cria o objeto da classe de indexação
index = Index(es, INDEX)

es.create_index(INDEX)
index.index_documents(FILE_PATH, ARRAY_NAME)
'''
index.index_documents_bulk(FILE_PATH, ARRAY_NAME)
queries = find_queries(QUERIES_PATH)


#Escreva as respostas encontrados no JSON
answers = find_answers(QUERIES_PATH)
output_answers_path = ".\\results\\answers.json"
with open(output_answers_path, 'w') as json_file:
    json.dump(answers, json_file, indent=4)

# Escreva os documentos encontrados no JSON
found_documents = linear_search(es, queries, SEARCHED_DOCUMENTS_QUANTITY)
output_file_path = ".\\results\\found.json"
with open(output_file_path, 'w') as json_file:
     json.dump(found_documents, json_file, indent=4)

# Carrega dados obtidos dos JSON para calcular precision@k e recall@k
with open('.\\results\\found.json', 'r') as found_file:
    found_documents = json.load(found_file)
with open('.\\results\\answers.json', 'r') as answers_file:
    answers = json.load(answers_file)

precision_at_k(found_documents, answers, 10)
recall_at_k(found_documents, answers, 10)

'''