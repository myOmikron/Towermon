from typing import Tuple

import pygame
from pygame import Surface
from pygame.surface import SurfaceType

from entities.navigation.Math.vector2 import Vector2

MAX_HEALTH = 100


class HealthBar:
    width: int
    height: int
    scale: float
    health: float
    alive: bool
    position: Vector2
    health_bar: Surface
    game_Screen: SurfaceType
    local_x: int
    current_health_width: int

    def __init__(self, game_screen: SurfaceType, width: int, height: int, health: float, position: Vector2):
        self.game_Screen = game_screen
        self.scale = 1
        self.health = health
        self.alive = True
        self.position = position
        self.health_bar = pygame.Surface((width, height))
        self.local_x = 0
        self.current_health_width = self.width

    def update_health(self, amount):
        self.health += amount
        if self.health <= 0:
            self.alive = False
            return
        self.local_x = int(self.local_x+(abs(amount)))
        self.current_health_width = int(self.width - abs(amount))
        rect = pygame.rect.Rect(self.local_x, 0, self.current_health_width, self.height)
        pygame.draw.rect(self.health_bar, (170, 15, 40), rect)

    def update(self, delta_time):
        ...

    def render(self, scale):
        ...
