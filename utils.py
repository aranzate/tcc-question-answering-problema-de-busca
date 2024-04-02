import json
import json
from datetime import datetime
from benchmark_recorder import *

def linear_search(es, queries, quantity):
    found_documents = {query.get('id_question'): [] for query in queries}
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
   
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
        
        results = calculate_action_execution_time(es.search, linear_search.__name__, timestamp, index="contextos", body=query_busca)
        
        found_documents[id].extend(hit['_id'] for hit in results['hits']['hits'])

    write_log(linear_search.__name__, "contextos do elastic search", es.search.__name__, found_documents, timestamp)
    
    return found_documents
    
# retorna o json de queries 
def find_queries(queries_file):
    with open(queries_file, 'r') as file:
        data = json.load(file)
        queries = data['questions']
    return queries

# retorna o json com a relação  <{ id_da_pergunta: [id_do_contexto_com_a_resposta] } >
def find_answers(queries_file):
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
