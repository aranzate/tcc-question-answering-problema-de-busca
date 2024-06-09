# tcc-question-answering-problema-de-busca

## Passos iniciais:
1. Instale o docker-compose
2. Instale as bibliotecas presentes no requirements.txt
3. Crie um arquivo chamado ```.env.local``` com as informações necessárias, seguindo o exemplo de ```.env.local.example```.
4. Crie as pastas que estão no .gitignore

### Inicialize o docker

1. Entre em uma das pastas com nome "Dockercompose"
2. Inicialize a instância com o comando:
```bash
sudo docker-compose up -d # inicializa os nós e o kibana
```
3. Para conferir se o kibana está executando, acesse: http://localhost:5601/app/discover
4. Na pasta do projeto, crie um arquivo ```.env``` e insira as chaves e variáveis de ambiente da instância do docker nele.

Obs.: para mais informações leia [README-DOCKER](./README-DOCKER.md)

### Execute a indexação

O arquivo ```indexing.py``` executará a indexação e salvará o resultado na pasta ```logs```.

1. Execute o arquivo indexing.py no terminal, seguindo um destes exemplos:
```bash
python3 indexing.py id   # index_documents
python3 indexing.py ib   # index_documents_bulk
```
2. Também é possível executar com os seguintes parâmetros:
- shards: quantidade de shards. Caso não seja passado, a quantidade de shards será estabelecida pela variável de ambiente SHARDS, do ```.env.local```.
- folder_name: nome da subpasta da pasta logs onde será guardado o log.
```bash
indexing.py [-h] func [shards] [folder_name]
```

### Execute a busca

O arquivo ```searching.py``` executará a busca de acordo com os parâmetros e salvará o resultado na pasta ```logs```.

1. Execute o arquivo searching.py no terminal, seguindo um destes exemplos:
```bash
python3 searching.py ls   # linear_search
python3 searching.py lm   # linear_msearch
python3 searching.py ps   # parallel_search
```

### Execute a comparação

O arquivo ```compare.py``` gerará os gráficos com resultados na pasta ```graficos```.

1. Execute o arquivo compare.py no terminal, seguindo um destes exemplos:
```bash
python3 compare.py 
```