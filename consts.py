system = "linux" # windows

INDEX = "contextos"
SHARDS = 7
NODES = 1
ARRAY_NAME = 'contexts'
SEARCHED_DOCUMENTS_QUANTITY = 10

LINEAR_SEARCH_PATH='linear_search_2024-05-28_22-50-44'
LINEAR_MSEARCH_PATH='linear_msearch_2024-05-28_22-21-53'
PARALLEL_SEARCH='parallel_search_2024-05-08_22-29-28'

if(system == "linux"):
    # FILE_PATH = "./ignorar/contexts.json"
    # QUERIES_PATH = "./ignorar/questions.json" 
    FILE_PATH = "./squad-v1.1-pt-master/contexts.json"
    QUERIES_PATH = "./squad-v1.1-pt-master/questions.json"
    RESULT_ANSWERS_PATH = "./results/answers.json"
    RESULT_FOUND_PATH = "./results/found.json"
    LOGS_PATH = "./logs/"
else:
    FILE_PATH = ".\\squad-v1.1-pt-master\\contexts.json"
    QUERIES_PATH = ".\\squad-v1.1-pt-master\\questions.json"
    RESULT_ANSWERS_PATH = ".\\results\\answers.json"
    RESULT_FOUND_PATH = ".\\results\\found.json"
    LOGS_PATH = ".\\logs\\"