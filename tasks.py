import time
from celery_app import celery_app

@celery_app.task(name="tasks.somar", queue="livros", bind=True)
def somar(self, a, b):
    time.sleep(3)
    return a + b

@celery_app.task(name="tasks.fatorial", bind=True)
def fatorial(self ,n):
    time.sleep(3)
    if n < 0:
        raise ValueError("Numero negativo")
    
    resultado = 1
    
    for i in range(2, n + 1):
        resultado *= i
        
    return resultado
        
    


# criar algumas tarefas
# rodar essas tarefas em background usando o Celery
# jogar essas tarefas para o redis, usando-o como sistema de filas