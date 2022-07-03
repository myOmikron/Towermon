import os
from typing import Tuple, List

import numpy as np
import pygame
from numpy.typing import NDArray


def load_png(name) -> pygame.Surface:
    """Loads an image from the assets

    :param name: Name of the file in assets/
    :return: Surface
    """
    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    return image


def load_tile_map(name: str, tile_dim: Tuple[int, int]) -> NDArray[NDArray[pygame.Surface]]:
    """
    Load a tilemap into single tiles
    :param name: name of the tilemap file
    :param tile_dim: dimension of on tile in the map
    :return: a List of the tiles
    """
    tile_map = load_png(name)
    tile_map_rect = tile_map.get_rect()
    w = tile_map_rect.width // tile_dim[0]
    h = tile_map_rect.height // tile_dim[1]
    array = np.ndarray((w, h)).astype(pygame.Surface)
    x, y = 0, 0
    for i in range(h):
        for j in range(w):
            array[i][j] = tile_map.subsurface((x, y, tile_dim[0], tile_dim[1]))
            x += tile_dim[0]
        x = 0
        y += tile_dim[1]
    return array


if __name__ == "__main__":
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    # Game init
    pygame.init()
    # Set fullscreen && double buffering for performance improvement
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF, 16)
    load_tile_map("trainer_TEAMROCKET_M.png", (32, 48))
