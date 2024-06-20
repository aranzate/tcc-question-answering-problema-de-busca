#!/bin/bash

source .env.local

nodes=$(python3 get_nodes.py)
shards_list=(2)

for shards in "${shards_list[@]}"; do
    # Nome da pasta com timestamp 
    # timestamp=$(date +"%Y-%m-%d_%H-%M-%S") 
    # folder_name=".${SEPARATOR_PATH}${LOGS_PATH}n${nodes}_s${shards}_${timestamp}"
    # mkdir "$folder_name"
    # folder_name="${folder_name}/"

    # Nome da pasta sem timestamp
    # folder_name=".${SEPARATOR_PATH}${LOGS_PATH}n${nodes}_s${shards}"
    # mkdir "$folder_name"
    # folder_name="${folder_name}/"

    # Sem pasta
    folder_name=""

    python3 indexing.py ib $shards $folder_name
    python3 searching.py ls $folder_name
    python3 searching.py lm $folder_name
    python3 searching.py ps $folder_name
    python3 compare.py $nodes $shards $folder_name
done


