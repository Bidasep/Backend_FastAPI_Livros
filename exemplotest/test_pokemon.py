from exemplotest.pokemon import calcular_pontos_ataque, pokemon_evoluiu
import pytest


"""def test_calcular_pontos_ataque():
    
    pokemon = {"forca_base": 10, "nivel": 1} 
    assert calcular_pontos_ataque(pokemon) == 10
    
    pokemon = {"forca_base": 5, "nivel": 0} 
    assert calcular_pontos_ataque(pokemon) == 0
    
    pokemon = {"forca_base": 20, "nivel": 5} 
    assert calcular_pontos_ataque(pokemon) == 100

def test_pokemon_evoluiu():
    pokemon = {"nivel": 15}
    nivel_evolucao = 20
    assert pokemon_evoluiu(pokemon, nivel_evolucao) == False
    
    
    pokemon = {"nivel": 20} 
    nivel_evolucao = 20
    assert pokemon_evoluiu(pokemon, nivel_evolucao) == True
    
    pokemon = {"nivel": 25}
    nivel_evolucao = 20
    assert pokemon_evoluiu(pokemon, nivel_evolucao) == True"""
    
    
#TESTE COM FIXTURES
@pytest.fixture
def bulbasaur():
    return {"nome":"bulbasaur", "forca_base": 49, "nivel": 10}
    
@pytest.fixture
def charmander():
    return {"nome":"charmander", "forca_base": 52, "nivel": 12} 

      
#recebe o pokemon Bulbasaur e compara os valores de nivel do pokemon com o nivel de evolucao  
def test_calcular_pontos_ataque_com_fixtures(bulbasaur):
    assert calcular_pontos_ataque(bulbasaur) == 490

#recebe o pokemon charmander e compara os valores de nivel do pokemon com o nivel de evolucao    
def test_pokemon_evolui_com_fixtures(charmander):
    
    #compara os valores de nivel do pokemon com o nivel de evolucao
    assert pokemon_evoluiu(charmander, 20) is False
    
    #compara os valores de nivel do pokemon com o nivel de evolucao
    assert pokemon_evoluiu(charmander, 12) is True