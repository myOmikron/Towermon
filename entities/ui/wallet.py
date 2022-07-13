import pygame
from pygame.surface import SurfaceType
from utils import image


class Wallet:
    coins: int

    def __init__(self, screen: SurfaceType):
        self.coins = 0
        self.font = pygame.font.SysFont("Arial", 50, bold=True)
        self.screen = screen

    def render(self):
        screen_width = self.screen.get_width()
        # pygame.draw.rect(self.screen, pygame.Color(255,255,255), pygame.Rect(screen_width-200,50,150,50))
        coin_img = image.load_png("AMULETCOIN.png")
        self.screen.blit(coin_img, (screen_width - 200, 102))

        font = pygame.font.Font("assets/Font/Gameplay.ttf", 20)
        text_surface = font.render(str(self.coins), True, (0, 0, 0))
        self.screen.blit(text_surface, (screen_width - 150, 115))
