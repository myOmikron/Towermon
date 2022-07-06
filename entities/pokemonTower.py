from JSON import jsonParser as parser
import entity, tile

class pokemonTower():
    def __init__(self, pokemonName: str, tile: tile):
        pokemonData = parser.getPokemonData(pokemonName)
        self.id = pokemonData["id"]
        self.name =pokemonData["name"]
        self.type = pokemonData["type"]

        self.tile = tile
        self.level = 1
        self.range = 10

#Stufenweise Verbesserung durch Münzen
def train(self):
    self.level += 1
    self.range += 2

#Greift einen Feind an, und zieht im Lebenspunkte ab
def attack(self, enemy: entity.enemy):
    factor = parser.getDamageFactor(self.type, enemy.type)
    damage = self.level * factor
    enemy.takeLife(damage)


