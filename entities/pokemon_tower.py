import time

import pygame.mixer

from json_utils import json_parser as parser
from entities import entity, tile
from pygame import Color, draw
from utils import image


class PokemonTower:
    def __init__(self, pokemon_name: str, x, y):
        pokemon_data = parser.get_pokemon_data(pokemon_name)
        self.id = pokemon_data["id"]
        self.name = pokemon_data["name"]
        self.type = pokemon_data["type"]
        self.x = x
        self.y = y

        self.level = 1
        self.range = 5
        self.rate = 2
        self.cost = 100

        self.last_attack = 0
        self.active = False

    # Stufenweise Verbesserung durch Münzen
    def train(self):
        self.level += 1
        self.range += 2
        self.rate += 1
        self.cost = self.cost + (2 * self.level)

    # Greift einen Feind an, und zieht im Lebenspunkte ab
    def attack(self, enemy: entity.Enemy):
        attack_sound = pygame.mixer.Sound('assets/audio/click.wav')
        current_time = time.time_ns()
        if abs(current_time - self.last_attack) > (1 / self.rate) * 1000000000:
            if self.in_range(enemy):
                print(enemy.life)
                self.active = True
                self.last_attack = time.time_ns()
                factor = parser.get_damage_factor(self.type, enemy.type)
                damage = self.level * factor
                enemy.take_life(damage)
                attack_sound.play()
            else:
                self.active = False


    def in_range(self, enemy: entity.Enemy):
        enemy_x = enemy.position.x
        enemy_y = enemy.position.y
        if abs(self.y - enemy_y) <= self.range and abs(self.x - enemy_x) <= self.range:
            return True
        else:
            return False

    def is_active(self):
        return self.active
