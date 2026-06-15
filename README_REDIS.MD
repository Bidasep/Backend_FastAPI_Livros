Redis Local:

1 - Instalar dependência:

    poetry add redis


2 - Executar a API:

    fastapi dev main.py

O sistema tentará conectar em:

localhost:6379

4 - Testar cache

    Listar livros:

    GET /livros


5 - Visualizar cache:


    GET /debug/redis

6 - adicionar livro

    POST /adiciona

7 - deletar livro

    DELETE /deletar/{id}