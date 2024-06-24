#!/bin/bash

# Realiza comparações e armazena tudo na pasta especificada em logs. 

source .env.local

nodes_list=(1 2 3 4)
shards_list=(1 2 4 8 12 16 32)

# Nome da pasta com timestamp 
# timestamp=$(date +"%Y-%m-%d_%H-%M-%S") 
# folder_name=".${SEPARATOR_PATH}${LOGS_PATH}_${timestamp}"
# mkdir "$folder_name"
# folder_name="${folder_name}/"

# Nome da pasta sem timestamp
# folder_name=".${SEPARATOR_PATH}${LOGS_PATH}"
# mkdir "$folder_name"
# folder_name="${folder_name}/"

# Sem pasta
# folder_name=""

# Nome da pasta personalizado
folder_name=".${SEPARATOR_PATH}${LOGS_PATH}contextos-0621"
mkdir "$folder_name"
folder_name="${folder_name}/"

for nodes in "${nodes_list[@]}"; do
    for shards in "${shards_list[@]}"; do
        python3 compare.py $nodes $shards $folder_name
    done
done


