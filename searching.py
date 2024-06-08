from search import Search
from utils import *
from metrics import *
import urllib3
import json
import consts

# desabilita avisos
urllib3.disable_warnings() 

# Cria objeto de busca no elastic search
es = Search()

queries = find_queries(consts.QUERIES_PATH)
#Escreva as respostas encontrados no JSON
answers = find_answers(consts.QUERIES_PATH)
output_answers_path = consts.RESULT_ANSWERS_PATH
with open(output_answers_path, 'w') as json_file:
    json.dump(answers, json_file, indent=4)

# Escreva os documentos encontrados no JSON
found_documents = linear_search(es, queries, consts.SEARCHED_DOCUMENTS_QUANTITY, consts.SHARDS, consts.NODES)
# found_documents = linear_msearch(es, queries, consts.SEARCHED_DOCUMENTS_QUANTITY, consts.SHARDS, consts.NODES)
# found_documents = parallel_search(es, queries, consts.SEARCHED_DOCUMENTS_QUANTITY, consts.SHARDS, consts.NODES)
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
