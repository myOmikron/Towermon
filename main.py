import sys

import pygame

import settings
from entities.level import Level
from entities.player import Player
from utils import image


class Game:
    def __init__(self):
        # Initialize the audio mixer
        pygame.mixer.pre_init(44100, 16, 2, 4096)

        # Game init
        pygame.init()

        # Set fullscreen && double buffering for performance improvement
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF, 16)

        # Set allowed events for performance improvement
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

        pygame.display.set_caption("Tower defense")
        pygame.display.set_icon(image.load_png("favicon.png"))

        self.clock = pygame.time.Clock()

        # Fill screen black
        self.screen.fill((0, 0, 0))

        self.scale = 1

        self.level = Level(self.scale)
        self.player = Player("player.png", self.scale)

    def run(self):
        move_north, move_south, move_west, move_east = False, False, False, False

        while True:
            # Trigger clock
            time_delta = self.clock.tick(settings.FPS_LOCK)/1000

            for event in pygame.event.get():
                # Handle quit event
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Handle zooming
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        if self.scale > 0.4:
                            self.scale /= 1.1
                    elif event.y > 0:
                        if self.scale < 2:
                            self.scale *= 1.1
                # Handle player move events
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        move_east = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_w:
                        move_north = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_a:
                        move_west = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_s:
                        move_south = event.type == pygame.KEYDOWN

            # Move player
            if move_east:
                # Only move if the opposite direction is not pressed
                if not move_west:
                    self.player.move_east(time_delta)
            elif move_west:
                self.player.move_west(time_delta)
            if move_north:
                # Only move if the opposite direction is not pressed
                if not move_south:
                    self.player.move_north(time_delta)
            elif move_south:
                self.player.move_south(time_delta)

            # Render map
            self.level.render(time_delta, self.scale)

            # Render player
            self.player.render(time_delta, self.scale)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
