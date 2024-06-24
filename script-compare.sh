#!/bin/bash

# Realiza comparações e armazena tudo na pasta especificada. 

source .env.local

folder_name=".${SEPARATOR_PATH}${LOGS_PATH}${FOLDER_PATH}"
mkdir "$folder_name"
folder_name="${folder_name}/"

for nodes in "${NODES_LIST[@]}"; do
    for shards in "${SHARDS_LIST[@]}"; do
        python3 compare.py $nodes $shards $folder_name
    done
done


