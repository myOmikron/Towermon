import time
from abc import ABC
from copy import deepcopy
from dataclasses import dataclass
import math
from typing import List, Union, Any

import pygame
from pygame.sprite import AbstractGroup
from pygame.surface import Surface, SurfaceType

from entities.navigation.Math.Vector2 import Vector2

import settings
import utils.image
import utils.transform

MAGIC_NUMBER = 0.04


@dataclass(slots=True)
class Entity:
    path: List[Vector2]
    position: Vector2 = None
    direction: Vector2 = None
    goal: Vector2 = None
    speed: float = 2
    at_goal: bool = False

    """
    Base Class for Entities, can follow a path
    """

    def angle_from_direction(self) -> int:
        """
        calculate the current angle in degrees from the direction vector
        :return: angle
        """
        return self.direction.angle_from_direction()

    def set_target(self, goal: Vector2) -> None:
        """
        Set the target you want to move to
        :param goal: you target destination
        :return: None
        """
        if self.position == goal:
            self.at_goal = True
            self.goal = goal
            return
        self.goal = goal
        self.direction = self.position.direction(goal)

    def move(self, delta_time):
        """
        move the entity by her speed and the given delta-time to the direction vector
        :param delta_time: float
        :return: None
        """
        self.position.update(self.direction, self.speed, delta_time)

    # TODO: add update to event-listener and removes it if the entity a at there goal to stop checking on update
    # or add custom tick system to minimize load
    def update(self, delta_time: float) -> None:
        """
        Update the entity movement at the given path
        :param delta_time: float
        :return: None
        """
        if self.at_goal:
            return
        self.move(delta_time)
        d = round(self.position.distance(self.goal), 3)
        if d <= MAGIC_NUMBER:
            self.position = self.goal
            if len(self.path) > 0:
                # print(f"Target updated: {self.path}")
                goal = self.path.pop(0)
                self.set_target(goal)
            else:
                self.at_goal = True


class Sprite(pygame.sprite.Sprite):
    """
    Generic Sprit Class for Pygame Surface
    """

    def __init__(self, image_path: str, position: Vector2, angle: float = 0, scale: float = 1):
        super(Sprite, self).__init__()
        self.image = utils.image.load_png(image_path)
        self.current_image = self.image
        self.rect = self.image.get_rect()
        self.screen = pygame.display.get_surface()
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
            img = utils.transform.rot_center(self.image, angle)
            self.current_image = pygame.transform.scale(img, (scaled_tile_size, scaled_tile_size))
            self.angle = angle
        if self.scale != scale:
            print(f"c scale: {self.angle} n scale: {angle}")
            img = utils.transform.rot_center(self.image, angle)
            self.current_image = pygame.transform.scale(img, (scaled_tile_size, scaled_tile_size))
            self.scale = scale
        self.screen.blit(self.current_image, (x, y))


class AnimatedSprite(pygame.sprite.Sprite):
    images: List[Surface]
    current_images: List[Surface]
    screen: Union[Surface, SurfaceType]
    index: int = 0
    last_delta_time: float = 0
    animation_speed: float = 0.1

    def __init__(self, images: List[Surface], position: Vector2, *groups: AbstractGroup, scale: float = 1):
        super().__init__(*groups)
        self.images = images
        self.position = position
        self.scale = scale
        self.screen = pygame.display.get_surface()
        self.current_images = self.images

    def update(self, delta_time: float, *args: Any, **kwargs: Any) -> None:
        if self.last_delta_time + delta_time >= self.animation_speed:
            if self.index < len(self.images)-1:
                self.index += 1
            else:
                self.index = 0
            self.last_delta_time = 0
        self.last_delta_time += delta_time

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
            self.current_images = [pygame.transform.scale(img, (self.images[0].get_width()*scale, self.images[0].get_height()*scale)) for img in self.images]
            self.scale = scale
        self.screen.blit(self.current_images[self.index], (x, y))


class Enemy(Entity, AnimatedSprite):
    """
    Base Class for Enemies
    consists of Entity and Sprite to combine movement with grafik
    """

    def __init__(self, position, path, images):
        Entity.__init__(self, path, position)
        AnimatedSprite.__init__(self, images, position)
        self.animation_speed = 1/(self.speed*3)

    def update(self, delta_time: float) -> None:
        Entity.update(self, delta_time)
        AnimatedSprite.update(self, delta_time)

    def render(self, scale: float) -> None:
        """
        render the enemy an update its direction angle
        :param scale: float
        :return: None
        """
        # angle = self.angle_from_direction()
        super().render(scale)


class EntityFactory(ABC):
    """Abstract Entity Factory"""

    def get_entity(self, position, path) -> Entity:
        """Returns a new Entity instance"""


class EnemyFactory(EntityFactory):
    scale: float
    images: List[Surface]
    """
    EnemyFactory, to create a new enemy type with the same image and only have a different position and path on 
    instantiation
    """

    def __init__(self, images, scale):
        self.images = images
        self.scale = scale

    def get_entity(self, position: Vector2, path: List[Vector2]) -> Entity:
        return Enemy(images=self.images, path=path, position=position)
