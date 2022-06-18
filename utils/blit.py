import pygame

import settings


def tile_blit(source: pygame.Surface, target: pygame.Surface, dest: (int, int)):
    """Blit based on tiles

    :param source: Surface to blit on
    :param target: Surface to blit
    :param dest: Tuple of x, y in tile size
    """
    source.blit(target, (dest[0]*settings.TILE_SIZE, dest[1]*settings.TILE_SIZE))
