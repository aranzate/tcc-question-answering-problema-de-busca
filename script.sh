#!/bin/bash

# Realiza a indexação, busca e comparações e armazena tudo na pasta logs. 
# Usará a quantidade de nodes da instância do docker ativa atualmente.

source .env.local

nodes=$(python3 get_nodes.py)
shards_list=$SHARDS_LIST

# Nome da pasta com timestamp 
# timestamp=$(date +"%Y-%m-%d_%H-%M-%S") 
# folder_name=".${SEPARATOR_PATH}${LOGS_PATH}${INDEX}_${timestamp}"
# mkdir "$folder_name"
# folder_name="${folder_name}${SEPARATOR_PATH}"

# Nome da pasta sem timestamp 
# folder_name=".${SEPARATOR_PATH}${LOGS_PATH}${INDEX}"
# mkdir "$folder_name"
# folder_name="${folder_name}${SEPARATOR_PATH}"

# Sem pasta
# folder_name=""

# Nome da pasta vem de .env.local
folder_name=".${SEPARATOR_PATH}${LOGS_PATH}${FOLDER_PATH}${SEPARATOR_PATH}"

for shards in "${shards_list[@]}"; do
    python3 indexing.py ib $shards $folder_name
    python3 searching.py ls $folder_name
    python3 searching.py lm $folder_name
    python3 searching.py ps $folder_name
    python3 compare.py $nodes $shards $folder_name
done


