# API de livros

#GET,POST,PUT,DELETE

# POST - ADICIONAR
# GET -  Buscar dados na API
# PUT - Atualizar informações
# Delete - Deletar informações 

from fastapi import FastAPI, HTTPException,Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os

app = FastAPI()

MEU_USUARIO = "admin"
MINHA_SENHA = "admin" 

security = HTTPBasic()

meus_livrozinhos = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int
    
def autenticar_meu_usuário(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.username, MINHA_SENHA)
    
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail= "Usuário ou senha incorretos",
            headers= {"WWW-Authenticate":"basic"}
        )

    
@app.get("/")
def hello_world():
    return {"Hellos" : "Worlds!"}

@app.get("/livros")
def get_livros(credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuário)):
    if not meus_livrozinhos:
        return {"message: ""Não existe nenhum livro!"}
    else:
        return{"livros": meus_livrozinhos}
    

@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuário)):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400, detail = "Esse livro já existe!")
    else:
        meus_livrozinhos[id_livro] =  livro.model_dump() #Pega as informações de todo o "Livro"
        return {"Mensagem": "O livro foi criado com sucesso"}
    
    
@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int , livro:Livro, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuário)):
    meu_livro = meus_livrozinhos.get(id_livro)
    if not meu_livro:
        return HTTPException(status_code=400, detail = "Esse livro nao foi encontrado")
    else:
        # joga as informações dentro do antigo dicionario (meus_livrozinhos)
        # e não dentro da referencia do antigo dicionário (meu livro)
        #Antigo dicionário != referencia antido dicionário
        meus_livrozinhos[id_livro] = livro.model_dump()
        return {"message" : "As informnações do seu livro foram atualizadas com sucesso!"}


@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int):
    if not meus_livrozinhos:
        return HTTPException(status_code=400, detail = "Esse livro nao foi encontrado")
    else:
        del meus_livrozinhos[id_livro]
        return{"message": "Seu livro foi deletado com sucesso"}
            
    
    
    