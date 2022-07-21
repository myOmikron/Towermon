from copy import deepcopy
from dataclasses import dataclass
from typing import List, Callable, Tuple

from entities.entity import Entity, Enemy
from entities.entity_factories import EntityFactory, EnemyFactory
from entities.navigation.Math.vector2 import Vector2


@dataclass(slots=True)
class EntitySpawner:
    position: Vector2
    path: List[Vector2]
    on_the_way: List[Entity]
    dead: List[Entity]
    spawned: List[Entity]
    factory: EntityFactory
    last_delta: float
    health_callback: Callable
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
            if isinstance(entity, Enemy):
                if entity.life <= 0:
                    self.dead.append(entity)
                    self.on_the_way.remove(entity)
            if len(entity.path) <= 0 and entity.at_goal:
                self.health_callback(-10)
                self.dead.append(entity)
                self.on_the_way.remove(entity)

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
                self.on_the_way.append(entity)
                self.last_delta = 0
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


@dataclass(slots=True)
class EnemySpawner(EntitySpawner):
    on_the_way: List[Enemy]
    dead: List[Enemy]
    spawned: List[Enemy]
    factory: EnemyFactory

    """
        Enemy Spawner, can spawn enemies, control their pathing and render them.
    """

    def render(self, scale: float, offset: Tuple[int, int]) -> None:
        """
        Render all the entities from the spawner
        :param offset: Offset of the camera
        :param scale: float
        :return: None
        """
        for entity in self.on_the_way:
            entity.render(scale, offset)
