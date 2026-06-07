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

from sqlalchemy import create_engine,Column, Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread" : False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


app = FastAPI()

MEU_USUARIO = os.getenv("MEU_USUARIO")
MINHA_SENHA = os.getenv("MINHA_SENHA")

security = HTTPBasic()

meus_livrozinhos = {}

class LivroDB(Base):
    __tablename__ = "Livros"
    id =Column(Integer, primary_key = True, index = True)
    nome_livro= Column(String, index = True)
    autor_livro= Column(String, index = True)
    ano_livro= Column(Integer)
    
class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int    
    
Base.metadata.create_all(bind=engine)

def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def autenticar_meu_usuário(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)
    
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
def get_livros(page: int=1, limit: int = 10, db: Session = Depends(sessao_db)  ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuário)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400,detail="page ou limit estão com valores inválidos!!!")
    
    #Função ja para trazer organizado os itens do DB , substitui a antigas função livros_paginados
    Livros = db.query(LivroDB).offset((page - 1)* limit).limit(limit).all()
    
    if not Livros:
        return {"message: ""Não existe nenhum livro!"}
    
    #Função para contar a quantidade de itens na tabela
    total_livros = db.query(LivroDB).count()
    

    return {
        "page": page,
        "limit": limit,
        "total": total_livros,
        #Faz um for in (para cada livro ou item do Livro ( que é os arquivos do nosso DB))
        "livros": [{"id": livro.id, "nome_livro": livro.nome_livro, "autor_livro":livro.autor_livro, "ano_livro": livro.autor_livro} for livro in Livros]
        
        }
    
    

@app.post("/adiciona")
def post_livros(livro: Livro, db:Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuário)):
    
    db_livro = db.query(LivroDB).filter(LivroDB.nome_livro == livro.nome_livro,LivroDB.autor_livro == livro.autor_livro).first()
    
    if db_livro:
        raise HTTPException(status_code=400, detail = "Esse livro já existe dentro do banco de dados!")
    
    novo_livro = LivroDB(nome_livro = livro.nome_livro, autor_livro = livro.autor_livro, ano_livro = livro.ano_livro)
    
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    
    
    return {"Mensagem": "O livro foi criado com sucesso"}

    
#atualiza    
@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int , livro:Livro, db:Session = Depends(sessao_db) , credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuário)):
    
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    
    if not db_livro:
        return HTTPException(status_code=400, detail = "Esse livro nao foi encontrado no banco de dados!")
    db_livro.nome_livro = livro.nome_livro
    db_livro.autor_livro = livro.autor_livro
    db_livro.ano_livro  = livro.ano_livro
    
    db.commit()
    db.refresh(db_livro)
    
    return {"message" : "As informnações do seu livro foram atualizadas com sucesso no banco de dados!"}


@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int, db:Session = Depends(sessao_db) , credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuário)):
    
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    
    if not db_livro:
        return HTTPException(status_code=400, detail = "Esse livro nao foi encontrado na base de dados")
    
    
    db.delete(db_livro)
    db.commit()
    
    return{"message": "Seu livro foi deletado com sucesso"}
            
    
    
    