

def calcular_pontos_ataque(pokemon: dict) -> int:
    """ calcular o poder de ataque baseado na força base e nivel do pokemon """
    return pokemon ["forca_base"] * pokemon["nivel"]


def pokemon_evoluiu(pokemon: dict, nivel_evolucao: int) -> bool:
    ## retorna true se o pokemon pode evoluir.
    return pokemon ["nivel"] >= nivel_evolucao






