import time

import pygame.mixer

import entities.entity
from json_utils import json_parser as parser
from entities import entity, tile
from pygame import Surface


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
                self.active = True
                self.last_attack = time.time_ns()
                factor = parser.get_damage_factor(self.type, enemy.type)
                damage = self.level * factor
                enemy.take_life(damage)
                attack_sound.play()
                return True
            else:
                self.active = False
                return False



    def in_range(self, enemy: entity.Enemy):
        enemy_x = enemy.position.x
        enemy_y = enemy.position.y
        if abs(self.y - enemy_y) <= self.range and abs(self.x - enemy_x) <= self.range:
            return True
        else:
            return False

    def is_active(self):
        return self.active

class Projectile():
    def __init__(self, pos, enemy_pos):
        self.pos = pos
        self.goal = enemy_pos
        self.radius = 3
        self.color = pygame.Color(255,0,0)
        self.path = self.calculate_points()

    def calculate_points(self):
        points = []
        x = self.pos[0]
        y = self.pos[1]
        goal_x = self.goal[0]
        goal_y = self.goal[1]
        delta_x = goal_x -x
        delta_y = goal_y - y
        interval_x = delta_x / 50
        interval_y = delta_y / 50
        i = 0
        while i <= 50:
            points.append((x + interval_x * i, y + interval_y * i))
            i+=1
        return points

    def move(self):
        if len(self.path) > 0:
            self.pos = self.path[0]
            self.path.pop(0)

    def render(self, surface: Surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)
        pygame.display.update()