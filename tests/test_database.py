import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, LivroDB, app
from fastapi.testclient import TestClient
import os

# configurar o banco de dados de teste
DATABASE_URL_TEST = "sqlite:///:memory:"
# criar engine e sessão para o banco de dados de teste
engine = create_engine(DATABASE_URL_TEST, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker (bind=engine)
# criar as tabelas no banco de dados de teste
Base.metadata.create_all(bind=engine)



client = TestClient(app)

@pytest.fixture(autouse=True)
#permite que o mock do redis seja usado em todos os testes, sem precisar chamá-lo 
# explicitamente em cada teste usando a fixture autouse=True, que faz com que o mock seja
# aplicado automaticamente a todos os testes 
def mock_redis(mocker):
    mock_redis_client = mocker.patch("main.redis_client", autospec=True)
    mock_redis_client.get.return_value = None
    
@pytest.fixture(scope="function")
#cria uma sessão de banco de dados para cada teste, garantindo que cada teste tenha um banco de dados limpo e isolado
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def test_get_livros():

    #faz uma requisição para a rota "/livros" com autenticação básica usando o usuário e senha 
    # definidos nas variáveis de ambiente e retorna a resposta da requisição no caso os livros cadastrados no banco de dados
    response = client.get("/livros", auth=("admin", "admin"))
    
    # verificar se a resposta tem status code 200
    assert response.status_code == 200
    
    #verificar se a resposta contém a lista de livros esperada
    livros = response.json()
    assert len(livros["livros"]) == 10
    assert livros["livros"][4]["nome_livro"] == "Palmeiras"
    assert livros["livros"][4]["autor_livro"] == "SEP"
    assert livros["livros"][4]["ano_livro"] == 1914