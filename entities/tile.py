from typing import List

import pygame
from pygame.sprite import AbstractGroup

from utils import image


class Tile(pygame.sprite.Sprite):
    """The base class for tiles.

    :param path: Path of the resource, relative to assets/
    :param pos: Tuple of int, int, marks position of the tile
    :param groups: List of AbstractGroups
    """
    def __init__(self, path: str, pos: (int, int), groups: List[AbstractGroup]):
        super().__init__(groups)
        self.image = image.load_png(path)
        self.rect = self.image.get_rect(topleft=pos)
