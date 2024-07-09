#!/bin/bash

# Realiza comparações e armazena tudo na pasta especificada. 

source .env.local

folder_name=".${SEPARATOR_PATH}${LOGS_PATH}${FOLDER_PATH}${SEPARATOR_PATH}"

nodes_list=($NODES_LIST)
shards_list=($SHARDS_LIST_ASC)

# gráficos de comparação um por um
# for nodes in "${NODES_LIST[@]}"; do
#     for shards in "${SHARDS_LIST[@]}"; do
#         python3 compare.py $nodes $shards $folder_name
#     done
# done

# gráficos de comparação gerais
python compare_results.py $folder_name --nodes_list "${nodes_list[@]}" --shards_list "${shards_list[@]}"