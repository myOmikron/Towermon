import math
from dataclasses import dataclass
from enum import IntEnum
from typing import Tuple, List

import numpy as np
import pygame
from numpy.typing import NDArray
from pygame.sprite import AbstractGroup
from pygame.surface import SurfaceType, Surface

import settings
import utils
from entities.entity_factories import EnemyFactory
from entities.navigation.Math.vector2 import Vector2
from entities.navigation.a_star import AStar
from entities.navigation.nav_mesh import NavMesh, Cell
from entities.spawners import EnemySpawner
from entities.tile import Tile, TileType
from utils import image


class Level:
    """The base class for the level.

    :param initial_scale: Initial scaling factor
    """

    scale: float
    width: int
    height: int
    screen: SurfaceType
    # Current level image with all  visible tiles
    current_screen: Surface
    spawns: List[EnemySpawner]
    target: Vector2
    map_gird: NDArray[NDArray[Tile]]
    tiles: NDArray[Surface]

    def __init__(self, width: int, height: int, *groups: AbstractGroup):
        self.scale = 0
        self.width = width
        self.height = height
        self.screen = pygame.display.get_surface()
        self.map_gird = np.ndarray((width, height)).astype(Tile)
        self.tiles = np.array(
            [image.load_png("grass.png"), image.load_png("stone_tile.png"), image.load_png("spawner.png"),
             image.load_png("pokal.png")])
        self.current_screen = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        # self.create_map()

    @classmethod
    def load_level(cls, name):
        with open(name, "r") as fp:
            grid = []
            spawns = []
            target = Vector2((0, 0))
            for y, line in enumerate(fp.readlines()):
                row = []
                for x, raw_tile in enumerate(line.split(" ")):
                    rw = raw_tile.split(";")
                    if len(rw) == 2:
                        surface_id = int(rw[1])
                        tile_type = TileType(int(rw[0]))
                        if tile_type == TileType.SPAWN:
                            spawns.append(Vector2((x, y)))
                        elif tile_type == TileType.TARGET:
                            target = Vector2((x, y))
                        position = Vector2((x * settings.TILE_SIZE, y * settings.TILE_SIZE))
                        row.append(Tile(surface_id, position, tile_type))
                grid.append(np.array(row))
        grid = np.array(grid)
        level = cls(*grid.shape)
        level.map_gird = grid

        cells = []
        for y in range(grid.shape[0]):
            row = []
            for x in range(grid.shape[1]):
                cell = Cell(Vector2((x, y)))
                if grid[y][x].tile_type == TileType.BLOCKED:
                    cell.passable = False
                else:
                    cell.passable = True
                cell.travel_cost = grid[y][x].score
                row.append(cell)
            cells.append(row)

        images = utils.image.load_tile_map("trainer_TEAMROCKET_M.png", (32, 48))
        enemy_factory = EnemyFactory(images, 1)

        nav_mesh = NavMesh(grid.shape[1], grid.shape[0], cells)

        paths = [nav_mesh.find_path(spawn, target, AStar) for spawn in spawns]

        print(paths)

        level.spawns = [
            EnemySpawner(dead=[], on_the_way=[], spawned=[], path=path, position=spawn, factory=enemy_factory,
                         last_delta=0) for spawn, path in zip(spawns, paths)]

        level.target = target
        return level

    def level_spawn(self):
        for sp in self.spawns:
            sp.spawn(100)

    def save_level(self, name):
        with open(name, "w") as fp:
            fp.write(f"{self.width},{self.height}\n")
            for y in range(self.height):
                fp.write("".join([f"{int(self.map_gird[y][x].tile_type)};{self.map_gird[y][x].surface_id} " for x in
                                  range(self.width)]) + "\n")

    def _calc_visible_tiles(self) -> Tuple[int, int]:
        """Calculates the amount of visible tiles for the screen.
            self.scale is used to determine to current scaling factor

        :return: Tuple of visible tiles in x and y direction
        """
        scaled_tile_size = round(settings.TILE_SIZE * self.scale)

        screen_width, screen_height = self.screen.get_size()

        num_x = math.ceil(screen_width / scaled_tile_size)
        num_y = math.ceil(screen_height / scaled_tile_size)
        return num_x, num_y

    def add_tile(self, tile: Tile, position: Vector2):
        """
        Add a tile to the given position on the map_grid
        :param tile: tile you want to add
        :param position: game world coordinates of the tile
        :return: 
        """
        self.map_gird[position.y][position.x] = tile
        scaled_tile_size = round(settings.TILE_SIZE * self.scale)
        self.current_screen.blit(
            pygame.transform.scale(
                self.tiles[self.map_gird[position.y][position.x].surface_id],
                (scaled_tile_size, scaled_tile_size)
            ),
            (
                position.x * scaled_tile_size,
                position.y * scaled_tile_size
            )
        )

    def create_map(self):
        """Renders a default map"""

        for y in range(self.height):
            for x in range(self.width):
                if y % 2 == 0:
                    self.map_gird[y][x] = Tile(1, Vector2((x * settings.TILE_SIZE, y * settings.TILE_SIZE)),
                                               TileType.BLOCKED)
                else:
                    self.map_gird[y][x] = Tile(0, Vector2((x * settings.TILE_SIZE, y * settings.TILE_SIZE)),
                                               TileType.EMPTY)
        x, y = 13, 2
        self.map_gird[y][x] = Tile(0, Vector2((x * settings.TILE_SIZE, y * settings.TILE_SIZE)),
                                   TileType.EMPTY)
        x, y = 0, 4
        self.map_gird[y][x] = Tile(0, Vector2((x * settings.TILE_SIZE, y * settings.TILE_SIZE)),
                                   TileType.EMPTY)
        x, y = 13, 6
        self.map_gird[y][x] = Tile(0, Vector2((x * settings.TILE_SIZE, y * settings.TILE_SIZE)),
                                   TileType.EMPTY)
        self._render(self.scale)

    def _render(self, scale: float):
        """Trigger a complete rerender."""
        if self.scale != scale:
            self.scale = scale
            num_x, num_y = self._calc_visible_tiles()
            scaled_tile_size = round(settings.TILE_SIZE * self.scale)
            self.current_screen.fill((68, 167, 169))
            for y in range(0, num_y + 2):
                for x in range(0, num_x + 2):
                    if x < self.height and y < self.width:
                        self.current_screen.blit(
                            pygame.transform.scale(
                                self.tiles[self.map_gird[y][x].surface_id],
                                (scaled_tile_size, scaled_tile_size)
                            ),
                            (
                                x * scaled_tile_size,
                                y * scaled_tile_size
                            )
                        )

    def update(self, delta_time: float):
        for spawner in self.spawns:
            spawner.update_spawn(delta_time, 0.4)
            spawner.update(delta_time)

    def render(self, time_delta: float, scale: float):
        """Render the level.

        :param time_delta: Time in seconds since the last render cycle
        :param scale: Scale factor
        """

        # TODO: Only rerender necessary parts
        self._render(scale)
        self.screen.blit(self.current_screen, (0, 0))
        for spawner in self.spawns:
            spawner.render(scale)

        # self.visible_sprites.draw(self.screen)
