# FastAPI - Gerenciador de Tarefas

API REST desenvolvida com FastAPI para gerenciamento de Livros, utilizando SQLite como banco de dados, SQLAlchemy como ORM e autenticação HTTP Basic.

## Funcionalidades

* Adicionar Livros
* Listar livros
* Atualizar livros
* Remover Livros
* Persistência de dados com SQLite
* Autenticação HTTP Basic
* Containerização com Docker

## Tecnologias Utilizadas

* Python 3.12
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Poetry
* Docker

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

```bash
docker-compose up --build -d
```

ou, em versões mais recentes:

```bash
docker compose up --build -d
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

MEU_USUARIO = "admin"
MINHA_SENHA = "admin" 

DATABASE_URL = "sqlite:///./livros.db"
PYTHONUNBUFFERED = 1

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

## Endpoints

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



### Atualizar tarefa

```http
PUT /atualiza/{id_livro}
```



### Remover Livro

```http
DELETE /deletar/{id_livro}
```

---

## Estrutura do Projeto

```text
.
├── main.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
├── livros.db
└── README.md
```

---

## Autor

Projeto desenvolvido para fins de estudo utilizando FastAPI, SQLAlchemy, SQLite e Docker.
desenvolvido por:

Everton Felipe
