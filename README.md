# FastAPI - Gerenciador de Livros com processamento assíncrono

API REST desenvolvida com FastAPI para gerenciamento de Livros, utilizando SQLite como banco de dados, SQLAlchemy como ORM e autenticação HTTP Basic,Kafka para mensageria e publicação de eventos.

## Funcionalidades

* Adicionar Livros
* Listar livros
* Atualizar livros
* Remover Livros
* Persistência de dados com SQLite
* Autenticação HTTP Basic
* Containerização com Docker
* Cache 
* Filas de mensagens e processamentos assíncronos.
* Serviços de mensageria e publicação de eventos.

## Tecnologias Utilizadas

* Python 3.12
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Poetry
* Docker
* Redis
* Celery
* Kafka

## Arquitetura

A aplicação utiliza FastAPI para disponibilizar a API REST.

- SQLite para persistência dos Dados.
- Redis como Broker e Backend de resultados.
- Celery para processamento assíncrono.
- Kafka para mensageria e publicação de eventos.
- Docker para containerização.

Fluxo das tarefas assíncronas:

Cliente → FastAPI → Redis → Celery Worker → Redis → Cliente

---

## Pré-requisitos

Antes de iniciar, certifique-se de possuir instalado:

* Docker
* Docker Compose

Verifique a instalação:

```bash
docker --version
docker compose version
```

---

## Clonando o Repositório

```bash
git clone https://github.com/Bidasep/Backend_FastAPI_Livros.git
cd Backend_FastAPI_Livros
```

---

## Construindo e Executando a Aplicação

Construir a imagem e iniciar os contêineres:


COMANDO PARA INICIAR O container
```
    1 - podman machine init
```
```
    2 - podman machine start
```
```
    3 - podman-compose build --no-cache
```
SUBIR O CONTAINER
```
    podman compose up -d
```

A aplicação ficará disponível em:

```text
http://localhost:8000
```

Documentação Swagger:

```text
http://localhost:8000/docs
```

Documentação ReDoc:

```text
http://localhost:8000/redoc
```

---

Criar o arquivo .env na pasta do projeto  com as variaveis de ambiente

```text

#VARIAVEIS DE AMBIENTE
DATABASE_URL = "sqlite:///./livros.db"

MEU_USUARIO = "admin"
MINHA_SENHA = "admin" 

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_URL=redis://redis:6379/0
KAFKA_SERVER=kafka:9092

```

## Encerrando a Aplicação

Para parar os contêineres:

```bash
docker-compose down
```

ou

```bash
docker compose down
```


---

## Credenciais de Acesso

A aplicação utiliza autenticação HTTP Basic.

Usuário:

```text
admin
```

Senha:

```text
admin
```

---

## Endpoints Via FASTAPI

exempo :

http://localhost:8000/livros
irá listar todos os livros

### Listar Livros

```http
GET /livros
```

### Adicionar Livro

```http
POST /adiciona
```

Exemplo de corpo da requisição:

```json
{
  "nome_Livro": "Palmeiras",
  "autor_livro": "SEP",
  "ano_livro": int
}
```


### Atualizar tarefa

```http
PUT /atualiza/{id_livro}
```



### Remover Livro

```http
DELETE /deletar/{id_livro}
```

### Efetuar SOMA E FATORIAL via fila TESTE CELERY E REDIS

Criar tarefa de soma

```http
POST "/calcular/soma"
```
Passar 2 numeros "a" e "b".

Exemplo de requisição:

``` http
POST /calcular/soma?a=2&b=4
```
Criar tarefa de Fatorial

```http
POST "/calcular/fatorial"
```
Passar 1 numero "N".

Exemplo de requisição:

``` http
POST /calcular/fatorial?n=5
```


### Verificar as Filas  e status das Tarefas enviadas.

``` http
GET /tarefas/recentes
```
Exemplo de retorno:

``` json
{
  "task_id": "5e4f9b...",
  "status": "SUCCESS",
  "resultado": 120
}
```


## Monitorando o Worker Celery

Verificar logs do worker:

```bash
podman logs -f celery-server
```

Exemplos de processamentos

    Task tasks.fatorial received //
    Task tasks.fatorial succeeded


```md
## Fila de Processamento

O worker Celery foi configurado para consumir a fila personalizada:

```text
livros
```

## Envio de mensagens e eventos para o Kafka.

A aplicação utiliza Apache Kafka para publicação de eventos relacionados às
 operações realizadas na API.

O ambiente inclui:

- Kafka Broker
- Zookeeper
- Kafka UI

a interface de monitoramento está inicialmente configurada para a porta 8080.
Para modificar a porta siga para o docker-compose e mude a porta:

```
    Serviços:
        kafka-ui:
            ports:
            - "8080:8080"
```

Kafka UI - Acesso a interface de monitoramento: Onde deverá colocar a porta Escolhida

```
http://localhost:8080
```

```http
POST /adiciona
```

Exemplo de corpo da requisição:

```json
{
  "nome_Livro": "Palmeiras",
  "autor_livro": "SEP",
  "ano_livro": int
}
```


## Estrutura do Projeto

```text
.
├── main.py
├── celery_app.py
├── tasks.py
├── kafka_producer.py
├── Dockerfile
├── docker-compose.yml
├── livros.db
├── README.md
└── .env
```

---

## Autor

Projeto desenvolvido para fins de estudo utilizando FastAPI, SQLAlchemy, SQLite , Redis, Celery, Kafka e Docker.
desenvolvido por:

## Everton Felipe

