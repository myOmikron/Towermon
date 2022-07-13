from dataclasses import dataclass
from typing import Tuple

import pygame
from pygame import Surface
from pygame.surface import SurfaceType

import settings

MAX_HEALTH = 100


@dataclass(slots=True)
class HealthBar:
    width: int
    height: int
    scale: float
    health: float
    alive: bool
    position: Tuple[int, int]
    health_bar: Surface
    current_health_bar: Surface
    game_screen: SurfaceType
    local_x: int
    current_health_width: int

    def __init__(self, game_screen: SurfaceType, width: int, height: int, health: float, position: Tuple[int, int]):
        """
        A Simple and scalable health bar
        :param game_screen: screen of the game
        :param width: width of the health bar
        :param height: height of the health bar
        :param health: amount of health
        :param position: position of the health bar on the game screen
        """
        self.width = width
        self.height = height
        self.game_screen = game_screen
        self.scale = 1
        self.health = health
        self.alive = True
        self.position = position
        self.health_bar = pygame.Surface((width, height))
        self.health_bar.fill((255, 255, 255))
        self.local_x = 0
        self.current_health_width = self.width
        self.update_health(0)
        self.current_health_bar = self.health_bar

    def _update_bar(self, amount):
        self.local_x = round(self.local_x + ((abs(amount) / MAX_HEALTH) * self.width))
        self.current_health_width = max(round(self.current_health_width - ((abs(amount) / MAX_HEALTH) * self.width)), 1)
        bar = pygame.surface.Surface((self.current_health_width, self.height))
        bar.fill((170, 15, 40))
        self.health_bar.fill((255, 255, 255))
        self.health_bar.blit(bar, (self.local_x, 0))
        self.current_health_bar = self.health_bar
        return bar, self.local_x

    def update_health(self, amount):
        """
        Update the health bar
        :param amount: amount of health that's getting removed
        :return:
        """
        if self.alive:
            self.health += amount
            if self.health <= 0:
                self.alive = False
                return self._update_bar(amount)
            return self._update_bar(amount)

    def update(self, delta_time):
        ...

    def render(self, scale):
        """
        render health bar on the game screen
        :param scale:
        :return:
        """
        x, y = self.position
        if self.scale != scale:
            self.scale = scale
            scaled_tile_size = round(settings.TILE_SIZE * scale)
            x = round(self.position[0] * scaled_tile_size)
            y = round(self.position[1] * scaled_tile_size)
            w, h = round(self.width * scale), round(self.height * scale)
            self.current_health_bar = pygame.transform.scale(self.health_bar, (w, h))
        self.game_screen.blit(self.current_health_bar, (x, y))
