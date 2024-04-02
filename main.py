from search import Search
from index import Index
import urllib3
import json

# desabilita avisos
urllib3.disable_warnings() 

# Inicializa variáveis globais
INDEX = "contextos"
FILE_PATH = ".\\squad-v1.1-pt-master\\contexts.json"
QUERIES_PATH = ".\\squad-v1.1-pt-master\\questions.json"
ARRAY_NAME = 'contexts'
SEARCHED_DOCUMENTS_QUANTITY = 10

# Cria objeto de busca no elastic search
es = Search()

# Cria o objeto da classe de indexação
index = Index(es, INDEX)

es.create_index(INDEX)
#index.index_documents(FILE_PATH, ARRAY_NAME)
index.index_documents_bulk(FILE_PATH, ARRAY_NAME)
queries = es.find_queries(QUERIES_PATH)


#Escreva as respostas encontrados no JSON
answers = es.find_answers(QUERIES_PATH)
output_answers_path = "answers.json"
with open(output_answers_path, 'w') as json_file:
    json.dump(answers, json_file, indent=4)

# Escreva os documentos encontrados no JSON
found_documents = es.linear_search(queries, SEARCHED_DOCUMENTS_QUANTITY)
output_file_path = "found.json"
with open(output_file_path, 'w') as json_file:
     json.dump(found_documents, json_file, indent=4)

# Carrega dados obtidos dos JSON para calcular precision@k e recall@k
with open('found.json', 'r') as found_file:
    found_documents = json.load(found_file)
with open('answers.json', 'r') as answers_file:
    answers = json.load(answers_file)

es.precision_at_k(found_documents, answers, 10)
es.recall_at_k(found_documents, answers, 10)

