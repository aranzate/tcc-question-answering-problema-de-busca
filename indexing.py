from search import Search
from index import Index
from utils import *
from metrics import *
import urllib3
import consts
urllib3.disable_warnings() 

es = Search()
index = Index(es, consts.INDEX)
es.create_index(consts.INDEX, consts.SHARDS)

# indexação linear
# index.index_documents(consts.FILE_PATH, consts.ARRAY_NAME, shards, nodes)

# indexação bulk
index.index_documents_bulk(consts.FILE_PATH, consts.ARRAY_NAME, consts.SHARDS, consts.NODES)


