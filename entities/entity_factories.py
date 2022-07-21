from abc import ABC
from typing import List

from pygame.sprite import AbstractGroup
from pygame.surface import Surface

from entities.entity import Entity, Enemy
from entities.navigation.Math.vector2 import Vector2


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

    def __init__(self, scale, *groups: AbstractGroup):
        self.scale = scale
        self.groups = groups

    def get_entity(self, position: Vector2, path: List[Vector2]) -> Enemy:
        return Enemy(path=path, position=position, *self.groups)
