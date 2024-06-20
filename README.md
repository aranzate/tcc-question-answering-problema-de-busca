# Passos iniciais:
1. Instale o docker-compose
2. Instale as bibliotecas presentes no requirements.txt
3. Crie um arquivo chamado ```.env.local``` com as informações necessárias, seguindo o exemplo de ```.env.local.example```.

## Inicialize o docker

1. Entre em uma das pastas com nome "Dockercompose"
2. Inicialize a instância com o comando:
```bash
sudo docker-compose up -d # inicializa os nós e o kibana
```
3. Para conferir se o kibana está executando, acesse: http://localhost:5601/app/discover
4. Na pasta do projeto, crie um arquivo ```.env``` e insira as chaves e variáveis de ambiente da instância do docker nele.

Obs.: para mais informações leia [README-DOCKER](./README-DOCKER.md)

## Execute de uma vez

O script ```script.sh``` executará a indexação, a busca e comparação e salvará os resultados na pasta ```/logs/n<nodes>_s<shards>```.

```bash
chmod +x script.sh
bash script.sh
```

## Execute separadamente

### Execute a indexação

O script ```indexing.py``` executará a indexação e salvará o resultado na pasta ```/logs```.

Os parâmetros são:
- func (obrigatório): função a ser executada. (id - index_documents, ib - index_documents_bulk)
- shards: quantidade de shards. Caso não seja passado, a quantidade de shards será estabelecida pela variável de ambiente SHARDS, do ```.env.local```.
- folder_name: nome da subpasta da pasta ```/logs``` onde será guardado o resultado.
```bash
indexing.py [-h] func [shards] [folder_name]
```

Os exemplos a seguir executam indexações e salvam os logs em ```/logs```:
```bash
python3 indexing.py id   # index_documents
python3 indexing.py ib   # index_documents_bulk
```

### Execute a busca

O script ```searching.py``` executará a busca de acordo com os parâmetros e salvará o resultado na pasta ```logs```.

Os parâmetros são:
- func (obrigatório): função a ser executada. (ls - linear_search, lm - linear_msearch, ps - parallel_search)
- folder_name: nome da subpasta da pasta ```/logs``` onde será guardado o resultado.
```bash
searching.py [-h] func [folder_name]
```

Os exemplos a seguir executam buscas e salvam os logs em ```/logs```:
```bash
python3 searching.py ls   # linear_search
python3 searching.py lm   # linear_msearch
python3 searching.py ps   # parallel_search
```

### Execute a comparação

O script ```compare.py``` fará a comparação e geração de gráficos para os arquivos de log do ```linear_search```, ```linear_msearch``` e ```parallel_search``` que estão dentro da pasta ```/logs```. Para isto é necessário já ter executado a "busca". 

Os parâmetros da execução são:
- nodes (obrigatório): quantidade de nodes do arquivo de log
- shards (obrigatório): quantidade de shards do arquivo de log
- folder_name: nome da subpasta da pasta ```/logs``` onde estão os logs e será guardado o resultado.
```bash
compare.py [-h] nodes shards [folder_name]
```

O exemplo a seguir fará comparações e gerará gráficos para os arquivos da pasta ```/logs``` de nomes: ```n1_s4_log_linear_search.json```, ```n1_s4_log_linear_msearch.json``` e ```n1_s4_log_parallel_search.json```.
```bash
python3 compare.py 1 4
```

