import os

system = os.getenv("SYSTEM")

INDEX = "contextos"
SHARDS = 7
ARRAY_NAME = 'contexts'
SEARCHED_DOCUMENTS_QUANTITY = 10

LINEAR_SEARCH_PATH = os.getenv("LINEAR_SEARCH_PATH")
LINEAR_MSEARCH_PATH = os.getenv("LINEAR_MSEARCH_PATH")
PARALLEL_SEARCH = os.getenv("PARALLEL_SEARCH")

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