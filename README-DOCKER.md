# Docker compose

Para executar esta instância do docker compose, mate todas as instâncias ativas do docker e execute:

## Inicializar instância do docker

Entre na pasta do docker compose e execute:

```bash
sudo docker-compose up -d
```

## Matando instâncias antigas no linux

Listar ids dos containers: 
```bash
sudo docker ps -aq
```
apagar instancia do container: 

```bash
sudo docker rm -fv <ID DO CONTAINER>
```
procura a porta: 
```bash
sudo lsof -i :9200
sudo lsof -i :5601
```

 mata ela: 
```bash
kill -15 <PID>
```

