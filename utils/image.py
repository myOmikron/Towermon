import os

import pygame


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
