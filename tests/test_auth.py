from fastapi.testclient import TestClient
from main import app
import os
import pytest

#importa o app da main.py e cria um cliente de teste para a aplicação FastAPI
cliente = TestClient(app)

#permitir que os testes usem variáveis de ambiente para autenticação, pega as variáveis de ambiente do os 
# e define os valores de usuário e senha para autenticação
os.environ["MEU_USUARIO"] = "admin"
os.environ["MINHA_SENHA"] = "admin"

#  o redis é sempre substituido por um mock, para que os testes não dependam de um servidor Redis real.
# ele usa automaticamente devido ao uso da fixture autouse=True, que faz com que o mock seja aplicado automaticamente a todos os testes
@pytest.fixture(autouse=True)
#permite que o mock do redis seja usado em todos os testes, sem precisar chamá-lo 
# explicitamente em cada teste usando a fixture autouse=True, que faz com que o mock seja
# aplicado automaticamente a todos os testes 
def mock_redis(mocker):
    mock_redis_client = mocker.patch("main.redis_client", autospec=True)
    mock_redis_client.get.return_value = None
    
    
def autenticacao_usuario_com_sucesso():
#faz uma requisição para a rota "/livros" com autenticação básica usando o usuário e senha 
# definidos nas variáveis de ambiente
    response = cliente.get(
        "/livros", 
        auth=("admin", "admin")
    )
    
    #verifica se a resposta da requisição tem o status code 200, indicando que a autenticação foi bem-sucedida
    assert response.status_code == 200 
    
def autenticacao_com_usuario_invalido():
#faz uma requisição para a rota "/livros" com autenticação básica usando o usuário inválido e senha 
# definidos nas variáveis de ambiente
    response = cliente.get(
        "/livros", 
        auth=("usuario_invalido", "admin")
    )
    
    #verifica se a resposta da requisição tem o status code 401, indicando que a autenticação falhou
    assert response.status_code == 401 
    assert response.json() ["detail"] ==  "Usuário ou senha incorretos"
    


def autenticacao_com_usuario_invalido():
#faz uma requisição para a rota "/livros" com autenticação básica usando o usuário inválido e senha 
# definidos nas variáveis de ambiente
    response = cliente.get(
        "/livros", 
        auth=("admin", "senha_invalida")
    )
    
    #verifica se a resposta da requisição tem o status code 401, indicando que a autenticação falhou
    assert response.status_code == 401 
    assert response.json() ["detail"] ==  "Usuário ou senha incorretos"