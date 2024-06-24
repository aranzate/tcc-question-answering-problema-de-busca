# Extrai perguntas

import json
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env.local'))
JSON_DATA_NAME = os.getenv("JSON_DATA_NAME")
SQUAD_PATH = os.getenv("SQUAD_PATH")

# Load JSON data from a file
with open(f'{SQUAD_PATH}{JSON_DATA_NAME}.json', 'r') as file:
    data = json.load(file)

# Extract contexts from the data
new_data = {"questions": []}
id_context = 1
id_question = 1

# Iterar sobre os dados originais para extrair perguntas e contextos
for item in data["data"]:
    for paragraph in item["paragraphs"]:
        context = paragraph["context"]
        for qa in paragraph["qas"]:
            question = qa["question"]
            q_id = qa["id"]
            # Adicionar a pergunta, o id do contexto e o contexto ao novo dicionário
            new_data["questions"].append({
                "question": question,
                "id_question": id_question,
                "id_context": id_context,
            })
            id_question += 1
        # Incrementar o id do contexto
        id_context += 1

# Write the new JSON data to a file
with open(f'{SQUAD_PATH}{JSON_DATA_NAME}-questions.json', 'w') as output_file:
    json.dump(new_data, output_file, indent=2)
