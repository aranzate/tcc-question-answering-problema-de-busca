# Extrai contextos

import json

# Load JSON data from a file
with open('dev-v1.1-pt-reestruturado.json', 'r') as file:
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
with open('contexts.json', 'w') as output_file:
    json.dump(contexts_with_titles2, output_file, indent=2)
