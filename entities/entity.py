from dataclasses import dataclass
from typing import List

from numpy.typing import NDArray
from pygame.sprite import AbstractGroup
from pygame.surface import Surface

from entities.navigation.Math.vector2 import Vector2
from entities.sprite import AnimatedSprite

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


class Enemy(Entity, AnimatedSprite):
    """
    Base Class for Enemies
    consists of Entity and Sprite to combine movement with grafik
    """

    def __init__(self, position: Vector2, path: List[Vector2], images: NDArray[NDArray[Surface]],
                 *groups: AbstractGroup):
        Entity.__init__(self, path, position)
        AnimatedSprite.__init__(self, images, position, *groups)
        self.animation_speed = 1 / (self.speed * 3)
        self.angle = 0

    def update(self, delta_time: float) -> None:
        Entity.update(self, delta_time)
        AnimatedSprite.update(self, delta_time)

    def render(self, scale: float) -> None:
        """
        render the enemy an update its direction angle
        :param scale: float
        :return: None
        """
        # TODO only change index_y if the direction has changed
        if self.direction.x == 0.0 and self.direction.y < 0:
            self.index_y = 3
        elif self.direction.x == 0.0 and self.direction.y > 0:
            self.index_y = 0
        elif self.direction.x < 0 and self.direction.y == 0.0:
            self.index_y = 1
        elif self.direction.x > 0 and self.direction.y == 0.0:
            self.index_y = 2

        super().render(scale)
