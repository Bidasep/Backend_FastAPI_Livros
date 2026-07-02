from tasks import somar, fatorial
from celery_app import celery_app

#testa a função somar.
def test_somar():
    
    # resultado recebe = somar.apply(args=[5,3]).get() que executa a função somar
    # com os argumentos 5 e 3 e obtém o resultado.
    resultado = somar.apply(args=[5,3]).get()
    
    #resultado esperao é 8, então o teste verifica se o resultado obtido é igual a 8.
    assert resultado == 8

def test_fatorial():
    #resultado recebe = função fatorial.apply(args=[5]).get() 
    # que executa a função com o argumento 5 e obtem o resultado.
    resultado = fatorial.apply(args=[5]).get()
    #resultado esperao é 120, então o teste verifica se o resultado obtido é igual a 120.
    assert resultado == 120
    
    #teste para verifcar se se o numero 0 retorna 1, que é o fatorial de 0.
    resultado = fatorial.apply(args=[0]).get()
    assert resultado == 1
    