# FastAPI - Gerenciador de Tarefas

API REST desenvolvida com FastAPI para gerenciamento de tarefas, utilizando SQLite como banco de dados, SQLAlchemy como ORM e autenticação HTTP Basic.

## Funcionalidades

* Adicionar tarefas
* Listar tarefas
* Atualizar tarefas
* Marcar tarefas como concluídas
* Remover tarefas
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

### Listar tarefas

```http
GET /tarefas
```

### Adicionar tarefa

```http
POST /adiciona
```

Exemplo de corpo da requisição:

```json
{
  "nome_tarefa": "Estudar FastAPI",
  "descricao_tarefa": "Praticar criação de APIs",
  "concluida": false
}
```

### Atualizar tarefa

```http
PUT /atualiza/{id_tarefa}
```

### Concluir tarefa

```http
PUT /atualiza/{id_tarefa}/concluir
```

### Remover tarefa

```http
DELETE /delete/{id_tarefa}
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
├── tarefas.db
└── README.md
```

---

## Autor

Projeto desenvolvido para fins de estudo utilizando FastAPI, SQLAlchemy, SQLite e Docker.
