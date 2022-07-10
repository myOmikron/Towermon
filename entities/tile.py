from dataclasses import dataclass
from enum import IntEnum

from entities.navigation.Math.vector2 import Vector2
from entities.navigation.nav_mesh import Cell


class TileType(IntEnum):
    EMPTY = 0
    BLOCKED = 1
    TURRET = 2
    SPAWN = 3
    TARGET = 4


@dataclass(slots=True)
class Tile(Cell):
    tile_type: TileType
    surface_id: int
    highlighted: bool

    def __init__(self, surface_id: int, position: Vector2, tile_type: TileType, score: int = 0):
        passable = True
        if tile_type == TileType.BLOCKED or tile_type == TileType.TURRET:
            passable = False
        Cell.__init__(self, position=position, visited=False, travel_cost=score, passable=passable)
        self.tile_type = tile_type
        self.surface_id = surface_id
        self.highlighted = False

    def __hash__(self):
        return Cell.__hash__(self)
