from fastapi.testclient import TestClient
from main import app

#importa o app da main.py e cria um cliente de teste para a aplicação FastAPI
client = TestClient(app)

#testa a rota /calcular/soma
def test_calcular_soma(mocker):
    #mocka a função somar.delay para simular o envio da tarefa para o Celery
    mock_somar_delay = mocker.patch("tasks.somar.delay")
    
    #mocka as funções redis_client.lpush e redis_client.ltrim para simular a interação com o Redis
    mock_redis_lpush = mocker.patch("main.redis_client.lpush")
    mock_redis_ltrim = mocker.patch("main.redis_client.ltrim")
    
    #define o valor de retorno do mock da função somar.delay para simular o ID da tarefa
    mock_somar_delay.return_value.id = "fake-task-id"
    
    #faz uma requisição POST para a rota "/calcular/soma" com os parâmetros a=5 e b=3
    response = client.post("/calcular/soma", params={"a": 5, "b": 3})
    
    #verifica se a função somar.delay foi chamada com os argumentos corretos (5 e 3)
    assert response.status_code == 200
    assert response.json() == {
        "task_id": "fake-task-id",
        "message": "Tarefa de soma enviada para execução"
    }
    
    #verifica se as funções redis_client.lpush e redis_client.ltrim foram chamadas corretamente
    mock_redis_lpush.assert_called_once()
    mock_redis_ltrim.assert_called_once()





#testa a rota /calcular/fatorial  
def test_calcular_fatorial(mocker):
    #mocka a função fatorial.delay para simular o envio da tarefa para o Celery
    mock_fatorial_delay = mocker.patch("tasks.fatorial.delay")
    
    #mocka as funções redis_client.lpush e redis_client.ltrim para simular a interação com o Redis
    mock_redis_lpush = mocker.patch("main.redis_client.lpush")
    mock_redis_ltrim = mocker.patch("main.redis_client.ltrim")
    
    #define o valor de retorno do mock da função fatorial.delay para simular o ID da tarefa
    mock_fatorial_delay.return_value.id = "fake-task-id"
    
    #faz uma requisição POST para a rota "/calcular/fatorial" com os parâmetros a=5 e b=3
    response = client.post("/calcular/fatorial", params={"n":5})
    
    #verifica se a função fatorial.delay foi chamada com os argumentos corretos (5)
    assert response.status_code == 200
    assert response.json() == {
        "task_id": "fake-task-id",
        "message" : "Tarefa fatorial enviada com sucesso"
    }
    
    #verifica se as funções redis_client.lpush e redis_client.ltrim foram chamadas corretamente
    mock_redis_lpush.assert_called_once()
    mock_redis_ltrim.assert_called_once()