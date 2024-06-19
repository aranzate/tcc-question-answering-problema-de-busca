#!/bin/bash

source .env.local

nodes=$(python3 get_nodes.py)
shards_list=(1 2 4 8 12 16 32)

for shards in "${shards_list[@]}"; do
    timestamp=$(date +"%Y-%m-%d_%H-%M-%S") 
    folder_name=".${SEPARATOR_PATH}${LOGS_PATH}${nodes}_nodes_${shards}_shards_${timestamp}"
    mkdir "$folder_name"
    folder_name="${folder_name}/"

    python3 indexing.py ib $shards $folder_name
    python3 searching.py ls $folder_name
    python3 searching.py lm $folder_name
    python3 searching.py ps $folder_name
    python3 compare.py $nodes $shards $folder_name
done


