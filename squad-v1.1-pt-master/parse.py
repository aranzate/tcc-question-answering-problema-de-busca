import json

# Load JSON data from a file
with open('dev-v1.1-pt-reestruturado.json', 'r') as file:
    data = json.load(file)

# Extract questions from the data
questions_list = []
for entry in data["data"]:
    for paragraph in entry["paragraphs"]:
        if "qas" in paragraph:
            for qa in paragraph["qas"]:
                if "question" in qa:
                    questions_list.append({"question": qa["question"]})

# Create a new JSON structure
result_data = {"questions": questions_list}

# Write the new JSON data to a file
with open('questions.json', 'w') as output_file:
    json.dump(result_data, output_file, indent=2)

# Write the new JSON data to a file
with open('questions.json', 'w') as output_file:
    json.dump(result_data, output_file, indent=2)