from dataclasses import dataclass
from enum import IntEnum

import pygame

from entities.navigation.Math.vector2 import Vector2


class TileType(IntEnum):
    EMPTY = 0
    BLOCKED = 1
    TURRET = 2
    SPAWN = 3
    TARGET = 4


@dataclass(slots=True)
class Tile:
    tile_type: TileType
    score: int
    surface_id: int
    position: Vector2

    def __init__(self, surface_id: int, position: pygame.Vector2, tile_type, score=0):
        self.tile_type = tile_type
        self.score = score
        self.surface_id = surface_id
        self.position = position
