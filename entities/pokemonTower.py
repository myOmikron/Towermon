import os

import JSON.towerParser as tP


class pokemonTower():
    def __init__(self, pokemonName: str):
        pokemonData = tP.getPokemonData(pokemonName)
        self.id = pokemonData["id"]
        self.name = pokemonData["name"]
        self.type = pokemonData["type"]
        self.level = 1


if __name__ == "__main__":
    # print(os.listdir())
    pokemon = pokemonTower("charmander")
    print(pokemon)
