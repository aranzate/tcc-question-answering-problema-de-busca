# Extrai contextos e perguntas

import json
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env.local'))
JSON_DATA_NAME = os.getenv("JSON_DATA_NAME")
SQUAD_PATH = os.getenv("SQUAD_PATH")

# Carregar dados JSON de um arquivo
with open(f'{SQUAD_PATH}{JSON_DATA_NAME}.json', 'r') as file:
    data = json.load(file)

context_id = 1
question_id = 1

contexts_with_titles = []
questions_with_contexts = []

# Extrair contextos e perguntas dos dados
for entry in data["data"]:
    title = entry["title"]
    for paragraph in entry["paragraphs"]:
        context = paragraph["context"]
        
        # Adicionar contexto com título à lista
        contexts_with_titles.append({"context_id": context_id, "title": title, "context": context})
        
        # Extrair perguntas associadas ao contexto
        for qa in paragraph["qas"]:
            question = qa["question"]
            q_id = qa["id"]
            
            # Adicionar pergunta com ID do contexto à lista
            questions_with_contexts.append({
                "question": question,
                "id_question": question_id,
                "id_context": context_id,
            })
            question_id += 1
        
        context_id += 1

# Criar novas estruturas JSON para contextos e perguntas
contexts_with_titles_json = {"contexts": contexts_with_titles}
questions_with_contexts_json = {"questions": questions_with_contexts}

# Escrever os novos dados JSON em arquivos
with open(f'{SQUAD_PATH}{JSON_DATA_NAME}-contexts.json', 'w') as output_file:
    json.dump(contexts_with_titles_json, output_file, indent=2)

with open(f'{SQUAD_PATH}{JSON_DATA_NAME}-questions.json', 'w') as output_file:
    json.dump(questions_with_contexts_json, output_file, indent=2)
