from dataclasses import dataclass
from typing import List
from copy import deepcopy

from entities.Entity import Entity, EntityFactory
from entities.navigation.Math.Vector2 import Vector2


@dataclass(slots=True)
class EntitySpawner:
    position: Vector2
    path: List[Vector2]
    on_the_way: List[Entity]
    dead: List[Entity]
    spawned: List[Entity]
    factory: EntityFactory
    last_delta: float = 0
    """
    Entity Spawner, can spawn entities and control their pathing
    """

    def update(self, delta_time: float) -> None:
        """
        update all the current entities from this spawner and remove them from the on_the_way list and append them to
        the dead list if the length of the path is less than 1
        :param delta_time: float
        :return: None
        """
        for entity in list(self.on_the_way):
            entity.update(delta_time)
            if len(entity.path) < 1:
                self.dead.append(entity)
                self.on_the_way.remove(entity)

    def render(self, scale: float) -> None:
        """
        Render all the entities from the spawner
        :param scale: float
        :return: None
        """
        for entity in reversed(self.on_the_way):
            entity.render(scale)

    def update_spawn(self, delta_time: float, frequenz: float):
        """
        Update the spawn, the spawner will send off an entity from the spawned list at frequent intervals
        :param delta_time: float
        :param frequenz: float
        :return: None
        """
        if len(self.spawned) > 0:
            if self.last_delta + delta_time >= frequenz:
                entity = self.spawned.pop()
                entity.path.pop(0)
                entity.set_target(entity.path.pop(0))
                entity.angle = entity.angle_from_direction()
                self.on_the_way.append(entity)
                return
            self.last_delta += delta_time

    def spawn(self, amount: int) -> None:
        """
        spawn an amount of entities to the spawn list
        :param amount: int
        :return: None
        """
        for _ in range(amount):
            entity = self.factory.get_entity(self.position.copy(), deepcopy(self.path))
            self.spawned.append(entity)
