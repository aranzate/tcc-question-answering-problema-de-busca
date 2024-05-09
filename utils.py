import json
import json
from datetime import datetime
from benchmark_recorder import *

def linear_search(es, queries, quantity, shards, nodes):
    
    found_documents = {query.get('id_question'): [] for query in queries}
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    actions = []
    start_time = time.time()
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
        
        action_time, results = calculate_execution_time(es.search, id, index="contextos", body=query_busca)
        action_time["hits"] = [hit['_id'] for hit in results['hits']['hits']]
        actions.append(action_time)

        found_documents[id].extend(hit['_id'] for hit in results['hits']['hits'])
        
    end_time = time.time()
    write_log(linear_search.__name__, "contextos do elastic search", es.search.__name__, actions, timestamp, shards=shards, nodes=nodes, time_python_function=end_time-start_time)
    return found_documents

def linear_msearch(es, queries, quantity, shards, nodes):
    
    found_documents = {query.get('id_question'): [] for query in queries}
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    actions = []

    msearch_body = []
    ids = []
    start_time = time.time()
    for query in queries:
        msearch_body = []
        ids = []
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

        msearch_body.append({"index": "contextos"})
        msearch_body.append(query_busca)
        ids.append(id)


        results = es.msearch(index="contextos", body=msearch_body)

        execution_times = msearch_execution_time(results, ids)

        for action_time, result in zip(execution_times, results['responses']):
            id = action_time["id"]
            action_time["hits"] = [hit['_id'] for hit in result['hits']['hits']]
            actions.append(action_time)
            found_documents[id].extend(hit['_id'] for hit in result['hits']['hits'])
    end_time = time.time()
    
    write_log(linear_msearch.__name__, "contextos do elastic search", "msearch", actions, timestamp, shards=shards, nodes=nodes, time_python_function=end_time-start_time)
    return found_documents

def parallel_search(es, queries, quantity, shards, nodes):
    found_documents = {query.get('id_question'): [] for query in queries}
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    actions = []

    msearch_body = []
    ids = []

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

        msearch_body.append({"index": "contextos"})
        msearch_body.append(query_busca)
        ids.append(id)

    start_time = time.time()
    results = es.msearch(index="contextos", body=msearch_body)
    end_time = time.time()
    execution_times = msearch_execution_time(results, ids)

    for action_time, result in zip(execution_times, results['responses']):
        id = action_time["id"]
        action_time["hits"] = [hit['_id'] for hit in result['hits']['hits']]
        actions.append(action_time)
        found_documents[id].extend(hit['_id'] for hit in result['hits']['hits'])

    write_log(parallel_search.__name__, "contextos do elastic search", "msearch", actions, timestamp, shards=shards, nodes=nodes, time_python_function=end_time-start_time)
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
