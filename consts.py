import os
from dotenv import load_dotenv
load_dotenv('.env.local')

INDEX = "contextos"
ARRAY_NAME = 'contexts'
SEARCHED_DOCUMENTS_QUANTITY = 10

SHARDS = os.getenv("SHARDS")

LINEAR_SEARCH_PATH = os.getenv("LINEAR_SEARCH_PATH")
LINEAR_MSEARCH_PATH = os.getenv("LINEAR_MSEARCH_PATH")
PARALLEL_SEARCH = os.getenv("PARALLEL_SEARCH")

FILE_PATH = os.getenv("FILE_PATH")
QUERIES_PATH = os.getenv("QUERIES_PATH")
RESULT_ANSWERS_PATH = os.getenv("RESULT_ANSWERS_PATH")
LOGS_PATH = os.getenv("LOGS_PATH")