from typing import Tuple

import pygame
from pygame import Surface
from pygame.font import Font
from pygame.surface import SurfaceType

import utils.image
from entities.ui.health_bar import HealthBar


class HUD:
    health_bar: HealthBar
    back_ground: Surface
    position: Tuple[int, int]
    game_screen: SurfaceType
    font: Font
    coins: int

    def __init__(self, game_screen: SurfaceType, position: Tuple[int, int]):
        """
        Create a Hud to display health and the coins fancy
        :param game_screen: screen of the game
        :param position: position of the hud on game screen
        """
        self.back_ground = utils.image.load_png("health_coin_barl.png")
        self.health_bar = HealthBar(game_screen, 251, 12, 100, (177, 40))
        self.coins = 0
        self.position = position
        self.game_screen = game_screen
        self.ui_screen = self.back_ground.copy()
        self.font = pygame.font.Font("assets/Font/Gameplay.ttf", 30)
        self.bar = None
        self.update_health(0)
        self.x_off = 0

    def update_health(self, amount: int):
        """
        Update the health
        :param amount: the amount of health that's getting removed
        :return:
        """
        if self.health_bar.alive:
            self.bar, self.x_off = self.health_bar.update_health(amount)
            self._draw()

    def _draw(self):
        self.ui_screen = self.back_ground.copy()
        x, y = self.health_bar.position
        self.ui_screen.blit(self.bar, (x + self.x_off, y))
        text = self.font.render(str(self.coins), True, (0, 0, 0))
        self.ui_screen.blit(text, (131, 81))

    def update_coins(self, amount: int) -> None:
        """
        update the visible amount of coins from the wallet
        :param amount: current amount of coins in the wallet
        :return:
        """
        self.coins = amount
        self._draw()

    def render(self, coins: int):
        self.game_screen.blit(self.ui_screen, self.position)
