from search import Search
from index import Index
import urllib3

# desabilita avisos
urllib3.disable_warnings() 

# Inicializa variáveis globais
INDEX = "contextos"
FILE_PATH = ".\\apagar.json" #".\\squad-v1.1-pt-master\\contexts.json" 
ARRAY_NAME = 'contexts'

# Cria objeto de busca no elastic search
es = Search()

# Cria o objeto da classe de indexação
index = Index(es, INDEX)

es.create_index(INDEX)
# index.index_documents(FILE_PATH, ARRAY_NAME)
index.index_documents_bulk(FILE_PATH, ARRAY_NAME)
