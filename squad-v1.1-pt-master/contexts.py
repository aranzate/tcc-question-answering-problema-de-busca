# Extrai contextos

import json
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env.local'))
JSON_DATA_NAME = os.getenv("JSON_DATA_NAME")
SQUAD_PATH = os.getenv("SQUAD_PATH")

# Load JSON data from a file
with open(f'{SQUAD_PATH}{JSON_DATA_NAME}.json', 'r') as file:
    data = json.load(file)
context_id = 1
# Extract contexts from the data
contexts_with_titles = []
for entry in data["data"]:
    title = entry["title"]
    for paragraph in entry["paragraphs"]:
        context = paragraph["context"]
        contexts_with_titles.append({"context_id": context_id, "title": title, "context": context})
        context_id += 1

# Create a new JSON structure for contexts
contexts_with_titles2 = {"contexts": contexts_with_titles}

# Write the new JSON data to a file
with open(f'{SQUAD_PATH}{JSON_DATA_NAME}-contexts.json', 'w') as output_file:
    json.dump(contexts_with_titles2, output_file, indent=2)
