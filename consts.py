import os
from dotenv import load_dotenv
load_dotenv('.env.local')

INDEX = os.getenv("INDEX")
ARRAY_NAME = 'contexts'
SEARCHED_DOCUMENTS_QUANTITY = 10

SHARDS = os.getenv("SHARDS")

FILE_PATH = os.getenv("FILE_PATH")
QUERIES_PATH = os.getenv("QUERIES_PATH")
RESULT_ANSWERS_PATH = os.getenv("RESULT_ANSWERS_PATH")
LOGS_PATH = os.getenv("LOGS_PATH")
SEPARATOR_PATH = os.getenv("SEPARATOR_PATH")