import sys

import pygame

from utils import image

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS_LOCK = 144


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower defense")
        pygame.display.set_icon(image.load_png("favicon.png"))

        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Fill screen black
            self.screen.fill((0, 0, 0))
            pygame.display.update()
            self.clock.tick(FPS_LOCK)


if __name__ == '__main__':
    game = Game()
    game.run()
