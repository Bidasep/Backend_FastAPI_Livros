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
import redis
import json

from sqlalchemy import create_engine,Column, Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import asyncio

# ativar quando usar docker
#DATABASE_URL = os.getenv("DATABASE_URL")
#MEU_USUARIO = os.getenv("MEU_USUARIO")
#MINHA_SENHA = os.getenv("MINHA_SENHA")

##utilizar quando for subir somente o FAST API comentar quando usar docker.
MEU_USUARIO = "admin"
MINHA_SENHA = "admin" 

DATABASE_URL = "sqlite:///./livros.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread" : False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#inicialização do redis obs. configuração para rodar localmente
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)


app = FastAPI()


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



# a funcção .dict  foi substituida pela .model_dumpo
# função para salvar os dados no Redis
async def salvar_livro_redis(livro_id: int, livro: Livro):
    redis_client.set(f"livro:{livro_id}", json.dumps(livro.model_dump()))
    
 # função para deletar os dados no Redis   
async def deletar_livro_redis(livro_id: int):
    redis_client.delete(f"livro:{livro_id}")
    
    
    
    
#iniciar Db   
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
async def hello_world():
    return {"Hellos" : "Worlds!"}

#################################### TESTANDO CHAMADAS EXTERNAS
async def chamadas_externas1():
    await asyncio.sleep(2)
    return "Resultado chamada 01"
    
async def chamadas_externas2():
    await asyncio.sleep(2)
    return "Resultado chamada 02"
    
async def chamadas_externas3():
    await asyncio.sleep(2) 
    return "Resultado chamada 03"

#função para teste de tarefa assincrona
@app.get("/testando-API")
async def testando_api():
    tarefa01 = asyncio.create_task( chamadas_externas1())
    tarefa02 = asyncio.create_task( chamadas_externas2())
    tarefa03 = asyncio.create_task( chamadas_externas3())
    
    resultado1 = await tarefa01
    resultado2 = await tarefa02
    resultado3 = await tarefa03
    
    return {"message":"todas as chamadas das API's foram concluidas com sucesso",
            "resultado": [resultado1, resultado2, resultado3]
            }
    



#função testando o Redis, ver os objetos que estão salvos no redis e o ttl
@app.get("/debug/redis")
async def ver_livros_redis():
    chaves = redis_client.keys("livros:*")
    livros = []
    
    for chave in chaves:
        valor = redis_client.get(chave)
        ttl = redis_client.ttl(chave)
        livros.append(
            {
            "chave" : chave, 
            "valor": json.loads(valor),
            "ttl": ttl
            }
        )
    
    return livros
        
    



@app.get("/livros")
async def get_livros( page: int=1, limit: int = 10, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuário)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400,detail="page ou limit estão com valores inválidos!!!")

    cache_key = f"livros:page={page}&limit={limit}"
    cached = redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    #Função ja para trazer organizado os itens do DB , substitui a antigas função livros_paginados
    livros = db.query(LivroDB).offset((page - 1)* limit).limit(limit).all()

    if not livros:
        return {"message: ""Não existe nenhum livro!"}

    #Função para contar a quantidade de itens na tabela
    total_livros = db.query(LivroDB).count()


    resposta = {
        "page": page,
        "limit": limit,
        "total": total_livros,
        #Faz um for in (para cada livro ou item do Livro ( que é os arquivos do nosso DB))
        "livros": [
            {
                "id": livro.id,
                "nome_livro": livro.nome_livro,
                "autor_livro":livro.autor_livro,
                "ano_livro": livro.ano_livro
                
            } for livro in livros
        ]
    }
    
    #cache key é o tempo para os dados sumirem do cache
    redis_client.setex(cache_key,30,json.dumps(resposta))
    
    return resposta    
        
    

@app.post("/adiciona")
async def post_livros(livro: Livro, db:Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuário)):
    
    db_livro = db.query(LivroDB).filter(LivroDB.nome_livro == livro.nome_livro,LivroDB.autor_livro == livro.autor_livro).first()
    
    if db_livro:
        raise HTTPException(status_code=400, detail = "Esse livro já existe dentro do banco de dados!")
    
    novo_livro = LivroDB(nome_livro = livro.nome_livro, autor_livro = livro.autor_livro, ano_livro = livro.ano_livro)
    
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    
    await salvar_livro_redis(novo_livro.id, livro )
    
    
    return {"Mensagem": "O livro foi criado com sucesso"}

    
#atualiza    
@app.put("/atualiza/{id_livro}")
async def put_livros(id_livro: int , livro:Livro, db:Session = Depends(sessao_db) , credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuário)):
    
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    
    if not db_livro:
        raise HTTPException(status_code=400, detail = "Esse livro nao foi encontrado no banco de dados!")
    db_livro.nome_livro = livro.nome_livro
    db_livro.autor_livro = livro.autor_livro
    db_livro.ano_livro  = livro.ano_livro
    
    db.commit()
    db.refresh(db_livro)
    
    return {"message" : "As informnações do seu livro foram atualizadas com sucesso no banco de dados!"}


@app.delete("/deletar/{id_livro}")
async def delete_livro(id_livro: int, db:Session = Depends(sessao_db) , credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuário)):
    
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    
    if not db_livro:
        raise HTTPException(status_code=400, detail = "Esse livro nao foi encontrado na base de dados")
    
    
    db.delete(db_livro)
    db.commit()
    
    await deletar_livro_redis(id_livro)
    
    return{"message": "Seu livro foi deletado com sucesso"}
            
    
    
    