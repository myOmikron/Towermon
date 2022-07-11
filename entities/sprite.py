from typing import Union, Any

import numpy as np
import pygame
from numpy.typing import NDArray
from pygame.sprite import AbstractGroup
from pygame.surface import Surface, SurfaceType

import settings
from entities.navigation.Math.vector2 import Vector2
from utils.image import load_png
from utils.transform import rot_center


class Sprite(pygame.sprite.Sprite):
    """
    Generic Sprit Class for Pygame Surface
    """

    def __init__(self, screen: SurfaceType, image: Surface, position: Vector2, angle: float = 0, scale: float = 1):
        super(Sprite, self).__init__()
        self.image = image
        self.current_image = self.image
        self.rect = self.image.get_rect()
        self.screen = screen
        self.position = position
        self.angle = angle
        self.scale = scale

    def render(self, scale: float, angle: int) -> None:
        """
        Render the sprit
        :param angle: float of the current angle in degree
        :param scale: float, current map scale
        :return: None
        """

        scaled_tile_size = round(settings.TILE_SIZE * scale)
        x = round(self.position.x * scaled_tile_size)
        y = round(self.position.y * scaled_tile_size)

        # only update the scale or the rotation if it really changed

        if self.angle != angle:
            print(f"c angle: {self.angle} n angle: {angle}")
            img = rot_center(self.image, angle)
            self.current_image = pygame.transform.scale(img, (scaled_tile_size, scaled_tile_size))
            self.angle = angle
        if self.scale != scale:
            print(f"c scale: {self.angle} n scale: {angle}")
            img = rot_center(self.image, angle)
            self.current_image = pygame.transform.scale(img, (scaled_tile_size, scaled_tile_size))
            self.scale = scale
        self.screen.blit(self.current_image, (x, y))


class AnimatedSprite(pygame.sprite.Sprite):
    images: NDArray[NDArray[Surface]]
    current_images: NDArray[NDArray[Surface]]
    screen: Union[Surface, SurfaceType]
    animation_speed: float
    index_x: int
    index_y: int
    last_delta_time: float

    def __init__(self, images: NDArray[NDArray[Surface]], position: Vector2, *groups: AbstractGroup, scale: float = 1):
        """
        Create an Animated Sprite
        :param images: 2d array of surfaces
        :param position: position of sprite in game world
        :param groups: sprite group
        :param scale: scale of the sprite
        """
        super().__init__(*groups)
        self.images = images
        self.position = position
        self.scale = scale
        self.screen = pygame.display.get_surface()
        self.current_images = self.images.copy()
        self.index_x = 0
        self.index_y = 0
        self.last_delta_time = 0

    def update(self, delta_time: float, *args: Any, **kwargs: Any) -> None:
        """
        Update the sprite animation and rotation
        :param delta_time:
        :param args:
        :param kwargs:
        :return:
        """
        if self.last_delta_time + delta_time >= self.animation_speed:
            if self.index_x < self.images.shape[0] - 1:
                self.index_x += 1
            else:
                self.index_x = 0
            self.last_delta_time = 0
        self.last_delta_time += delta_time

    @staticmethod
    def _scale(img, width, height):
        return pygame.transform.scale(img, (width, height))

    @staticmethod
    def vectorize_scale(x, w, h):
        """
        Vectorized Scale to run it in parallel on all sprites for the animation
        :param x: the image to scale
        :param w: destination width
        :param h: destination height
        :return:
        """
        return np.vectorize(AnimatedSprite._scale)(x, w, h)

    def render(self, scale: float) -> None:
        """
        Render the sprit
        :param scale: float, current map scale
        :return: None
        """

        scaled_tile_size = round(settings.TILE_SIZE * scale)
        x = round(self.position.x * scaled_tile_size)
        y = round(self.position.y * scaled_tile_size)

        # only update the scale or the rotation if it really changed
        if self.scale != scale:
            w, h = round(self.images[0][0].get_width() * scale), round(self.images[0][0].get_height() * scale)
            self.current_images = AnimatedSprite.vectorize_scale(self.images, w, h)
            self.scale = scale
        self.screen.blit(self.current_images[self.index_y][self.index_x], (x, y))
