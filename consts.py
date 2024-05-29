system = "linux" # windows

INDEX = "contextos"
SHARDS = 7
NODES = 1
ARRAY_NAME = 'contexts'
SEARCHED_DOCUMENTS_QUANTITY = 10

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