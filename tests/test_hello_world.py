from fastapi.testclient import TestClient
from main import app



#importa o app da main.py e cria um cliente de teste para a aplicação FastAPI
client = TestClient(app)

def test_hello_world():
    #faz uma requisição GET para a rota raiz ("/") da aplicação FastAPI,
    # response será o objeto de resposta retornado pela aplicação
    response = client.get("/")
    
    #verifica se o status code da resposta é 200 (OK)
    assert response.status_code == 200
    
    #verifica se o conteúdo da resposta é igual a {"Hellos": "Worlds!"}
    assert response.json() == {"Hellos": "Worlds!"}