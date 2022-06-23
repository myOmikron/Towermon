import math
from typing import Tuple

import pygame

import settings
from utils import image


class Level:
    """The base class for the level.

    :param initial_scale: Initial scaling factor
    """
    def __init__(self, initial_scale):
        self.scale = initial_scale

        self.screen = pygame.display.get_surface()

        self.background = []
        self.visible_sprites = pygame.sprite.Group()

        self.create_map()

    def _calc_visible_tiles(self) -> Tuple[int, int]:
        """Calculates the amount of visible tiles for the screen.
            self.scale is used to determine to current scaling factor

        :return: Tuple of visible tiles in x and y direction
        """
        scaled_tile_size = round(settings.TILE_SIZE * self.scale)

        screen_width, screen_height = self.screen.get_size()

        num_x = math.ceil(screen_width / scaled_tile_size)
        num_y = math.ceil(screen_height / scaled_tile_size)
        return num_x, num_y

    def create_map(self):
        """Renders a default map"""
        grass_block = image.load_png("grass.png")

        for row_index, row in enumerate([[y for y in range(settings.LEVEL_HEIGHT)] for x in range(settings.LEVEL_WIDTH)]):
            c = []
            for column_index, column in enumerate(row):
                c.append(grass_block)
            self.background.append(c)
        self._render()

    def _render(self):
        """Trigger a complete rerender."""
        num_x, num_y = self._calc_visible_tiles()
        scaled_tile_size = round(settings.TILE_SIZE * self.scale)

        self.screen.fill((0, 0, 0))

        for x in range(0, num_x + 2):
            for y in range(0, num_y + 2):
                self.screen.blit(
                    pygame.transform.scale(
                        self.background[x][y],
                        (scaled_tile_size, scaled_tile_size)
                    ),
                    (
                        x * scaled_tile_size,
                        y * scaled_tile_size
                    )
                )

    def render(self, time_delta: float, scale: float):
        """Render the level.

        :param time_delta: Time in seconds since the last render cycle
        :param scale: Scale factor
        """
        # Check if scale has changed
        if scale != self.scale:
            self.scale = scale

        # TODO: Only rerender necessary parts
        self._render()

        self.visible_sprites.draw(self.screen)
