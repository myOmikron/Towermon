from abc import ABC
from dataclasses import dataclass
import math
from typing import List

import pygame
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

    def angle_from_direction(self) -> float:
        """
        calculate the current angle in degrees from the direction vector
        :return: angle
        """
        return self.position.angle_from_direction()

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

    def __init__(self, image_path: str, initial_scale: float, position: Vector2, angle: float = 0):
        super(Sprite, self).__init__()
        self.image = utils.image.load_png(image_path)
        self.rect = self.image.get_rect()
        self.screen = pygame.display.get_surface()
        self.position = position
        self.scale = initial_scale
        self.angle = angle

    def render(self, scale: float) -> None:
        """
        Render the sprit
        :param scale: float, current map scale
        :return: None
        """
        if self.scale != scale:
            self.scale = scale

        scaled_tile_size = round(settings.TILE_SIZE * scale)
        x = round(self.position.x * scaled_tile_size)
        y = round(self.position.y * scaled_tile_size)

        scaled_tile_size = round(settings.TILE_SIZE * scale)
        img = utils.transform.rot_center(self.image, self.angle)
        img = pygame.transform.scale(img, (scaled_tile_size, scaled_tile_size))
        self.screen.blit(img, (x, y))


class Enemy(Entity, Sprite):
    """
    Base Class for Enemies
    consists of Entity and Sprite to combine movement with grafik
    """

    def __init__(self, position, path, image_path, scale):
        Entity.__init__(self, path, position)
        Sprite.__init__(self, image_path, scale, position)

    def render(self, scale: float) -> None:
        """
        render the enemy an update its direction angle
        :param scale: float
        :return: None
        """
        self.angle = self.angle_from_direction()
        super().render(scale)


class EntityFactory(ABC):
    """Abstract Entity Factory"""

    def get_entity(self, position, path) -> Entity:
        """Returns a new Entity instance"""


class EnemyFactory(EntityFactory):
    scale: float
    image_path: str
    """
    EnemyFactory, to create a new enemy type with the same image and only have a different position and path on 
    instantiation
    """

    def __init__(self, image_path, scale):
        self.image_path = image_path
        self.scale = scale

    def get_entity(self, position, path) -> Entity:
        return Enemy(image_path=self.image_path, scale=self.scale, path=path, position=position)
