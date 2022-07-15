from json_utils import json_parser as parser
from entities import entity, tile
from pygame import Color, draw
from utils import image


class PokemonTower:
    def __init__(self, pokemon_name: str):
        pokemon_data = parser.get_pokemon_data(pokemon_name)
        self.id = pokemon_data["id"]
        self.name = pokemon_data["name"]
        self.type = pokemon_data["type"]

        self.level = 1
        self.range = 10
        self.rate = 2
        self.cost = 100

    # Stufenweise Verbesserung durch Münzen
    def train(self):
        self.level += 1
        self.range += 2
        self.rate += 1
        self.cost = self.cost + (2*self.level)

    # Greift einen Feind an, und zieht im Lebenspunkte ab
    def attack(self, enemy: entity.Enemy):
        factor = parser.get_damage_factor(self.type, enemy.type)
        damage = self.level * factor
        enemy.take_life(damage)

    def get_image(self):
        img = image.load_png(self.name + '.png')
        return img


class Projectile:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.radius = 3
        self.color = Color(255, 0, 0)

    def draw_projectile(self, surface):
        draw.circle(surface, self.color, (self.x, self.y), self.radius)
