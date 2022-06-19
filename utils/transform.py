import pygame


def rot_center(image: pygame.Surface, angle: float) -> pygame.Surface:
    """Rotate an image while keeping its center and size.

    :param image: Surface to rotate.
    :param angle: Angle to rotate (in deg)
    :return: Rotated surface
    """
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
