from JSON import jsonParser as parser
from entities import entity, tile
from pygame import Color, draw
from utils import image


class PokemonTower():
    def __init__(self, pokemonName: str, tile: tile):
        pokemonData = parser.getPokemonData(pokemonName)
        self.id = pokemonData["id"]
        self.name =pokemonData["name"]
        self.type = pokemonData["type"]

        self.tile = tile
        self.level = 1
        self.range = 10
        self.rate = 2

    #Stufenweise Verbesserung durch Münzen
    def train(self):
        self.level += 1
        self.range += 2
        self.rate += 1

    #Greift einen Feind an, und zieht im Lebenspunkte ab
    def attack(self, enemy: entity.Enemy):
        factor = parser.getDamageFactor(self.type, enemy.type)
        damage = self.level * factor
        enemy.takeLife(damage)

    def getImage(pokemonName: str):
        return image.load_png(pokemonName+'.png')

class Projectile():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.radius = 3
        self.color = Color(255,0,0)
    def drawProjectile(self, surface):
        draw.circle(surface,self.color, (self.x, self.y, self.radius))