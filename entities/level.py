import math
import pickle
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
from entities.navigation.nav_mesh import NavMesh
from entities.spawners import EnemySpawner
from entities.tile import Tile, TileType
from entities.pokemon_tower import PokemonTower
from entities.wallet import Wallet
from utils import image


class Map:
    width: int
    height: int
    scale: float
    game_screen: SurfaceType
    map_screen: Surface
    grid: NDArray[NDArray[Tile]]
    towers: NDArray[NDArray[PokemonTower]]
    tiles: NDArray[Surface]
    spawns: List[Vector2]
    target: Vector2
    high_light: Surface
    """Map for the Level"""

    def __init__(self, width, height, game_screen, grid, tiles, spawns, target):
        self.width = width
        self.height = height
        self.scale = 0.9
        self.game_screen = game_screen
        self.map_screen = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.grid = grid
        self.towers = np.ndarray(shape=grid.shape)
        self.tiles = tiles
        self.spawns = spawns
        self.target = target
        self.high_light = utils.image.load_png("highlight.png")

    def add_tile(self, tile: Tile, position: Vector2):
        """
        Add a tile to the given position on the map_grid
        :param tile: tile you want to add
        :param position: game world coordinates of the tile
        :return:
        """
        self.grid[position.y][position.x] = tile
        self._render_tile((int(position.x), int(position.y)))

    def _render_tower(self, position: Tuple[int, int]):
        x, y = position
        tower = self.towers[y][x]
        self._render_tile(tower.get_image, position)

    def _render_tile_from_grid(self, position: Tuple[int, int]):
        x, y = position
        tile = self.grid[y][x]
        self._render_tile(self.tiles[tile.surface_id], position)
        if tile.highlighted:
            self._render_tile(self.high_light, position)

    def _render_tile(self, surface, position: Tuple[int, int]) -> None:
        """
        Render tile from grid on map_surface
        :param position: position of the tile in grid
        :return:
        """
        x, y = position
        scaled_tile_size = round(settings.TILE_SIZE * self.scale)
        self.map_screen.blit(
            pygame.transform.scale(
                surface,
                (scaled_tile_size, scaled_tile_size)
            ),
            (
                x * scaled_tile_size,
                y * scaled_tile_size
            )
        )


    def _calc_visible_tiles(self) -> Tuple[int, int]:
        """Calculates the amount of visible tiles for the screen.
            self.scale is used to determine to current scaling factor

        :return: Tuple of visible tiles in x and y direction
        """
        scaled_tile_size = round(settings.TILE_SIZE * self.scale)
        screen_width, screen_height = self.game_screen.get_size()

        num_x = math.ceil(screen_width / scaled_tile_size)
        num_y = math.ceil(screen_height / scaled_tile_size)
        return num_x, num_y

    def _render(self, scale: float) -> None:
        """Trigger a complete rerender."""
        if self.scale != scale:
            self.scale = scale
            num_x, num_y = self._calc_visible_tiles()
            self.map_screen.fill((68, 167, 169))
            for y in range(0, num_y + 2):
                for x in range(0, num_x + 2):
                    if x < self.height and y < self.width:
                        self._render_tile_from_grid((x, y))
                        if isinstance(self.towers[y][x], PokemonTower):
                            self._render_tower((x, y))

    def update(self, delta_time: float) -> None:
        ...

    def render(self, scale: float) -> None:
        """Render the level.
        :param scale: Scale factor
        """
        self._render(scale)
        self.game_screen.blit(self.map_screen, (0, 0))


class Timer:
    duration: float
    finished: bool
    position: Vector2

    """
    A Simple Timer
    """

    def __init__(self, duration: float, position: Vector2, screen: SurfaceType):
        self.duration = duration
        self.finished = False
        self.position = position
        self.font = pygame.font.SysFont("Arial", 50, bold=True)
        self.screen = screen

    def render(self, scale):
        if not self.finished:
            time = str(f"{self.duration:.2f}")
            time = self.font.render(time, True, pygame.Color("RED"))
            self.screen.blit(time, (int(self.position.x), int(self.position.y)))

    def update(self, delta_time):
        if not self.finished:
            self.duration -= delta_time
            if self.duration <= 0:
                self.finished = True


class Level:
    """
    The base class for the level.
    """

    scale: float
    spawners: List[EnemySpawner]
    target: Vector2
    map: Map
    timer: Timer
    coins: Wallet
    wave_done: bool
    spawn_frequenz: float = 1
    stage: int = 0

    def __init__(self, width: int, height: int, game_screen: SurfaceType, map: Map, *groups: AbstractGroup):
        self.scale = 0.9
        self.tiles = np.array([
            image.load_png("grass.png"),
            image.load_png("stone_grass.png"),
            image.load_png("spawner.png"),
            image.load_png("pokal.png")
        ])
        self.map = map
        self.target = map.target
        self.wave_done = False

        enemy_factory = EnemyFactory(1)
        nav_mesh = NavMesh(height, width, map.grid)

        paths = [nav_mesh.find_path(spawn, map.target, AStar) for spawn in map.spawns]

        self.spawners = [EnemySpawner(
            dead=[],
            on_the_way=[],
            spawned=[],
            path=path,
            position=spawn,
            factory=enemy_factory,
            last_delta=0)
            for spawn, path in zip(map.spawns, paths)]

    def start(self, screen):
        """
        Start the level
        :param screen: game screen
        :return:
        """
        self.timer = Timer(10, Vector2(((settings.SCREEN_WIDTH // 2) - 100, 10)), screen)
        self.coins = Wallet(screen)

    @staticmethod
    def _pixel_to_grid_coord(x: int, y: int, scale) -> Tuple[int, int]:
        """
        convert pixel coordinates to grid coordinates
        :param x: pixel coord
        :param y: pixel coord
        :param scale: current map scale
        :return: (grid_x, grid_y)
        """
        scaled_tile_size = round(settings.TILE_SIZE * scale)
        x = x // scaled_tile_size
        y = y // scaled_tile_size
        return x, y

    @staticmethod
    def _grid_to_pixel_coord(x, y, scale):
        """
        convert grid coordinates to pixel coordinates
        :param x: grid coord
        :param y: grid coord
        :param scale: current map scale
        :return: (pixel_x, pixel_y)
        """
        scaled_tile_size = round(settings.TILE_SIZE * scale)
        x = round(x * scaled_tile_size)
        y = round(y * scaled_tile_size)
        return x, y

    @classmethod
    def load_level(cls, name):
        """
        Load a level from fiel TODO: refactoring
        :param name: name of the level file
        :return: Level object
        """
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
                        position = Vector2((x, y))
                        row.append(Tile(surface_id, position, tile_type))
                grid.append(np.array(row))
        grid = np.array(grid)

        tiles = np.array([
            image.load_png("grass.png"),
            image.load_png("stone_grass.png"),
            image.load_png("spawner.png"),
            image.load_png("pokal.png")
        ])

        map = Map(grid.shape[0], grid.shape[1], pygame.display.get_surface(), grid, tiles, spawns, target)

        level = Level(grid.shape[0], grid.shape[1], pygame.display.get_surface(), map)

        images = utils.image.load_tile_map("trainer_TEAMROCKET_M.png", (32, 48))
        enemy_factory = EnemyFactory(images, 1)
        nav_mesh = NavMesh(grid.shape[1], grid.shape[0], grid)

        paths = [nav_mesh.find_path(spawn, target, AStar) for spawn in spawns]

        level.spawns = [
            EnemySpawner(dead=[], on_the_way=[], spawned=[], path=path, position=spawn, factory=enemy_factory,
                         last_delta=0) for spawn, path in zip(spawns, paths)]

        level.target = target
        # level.render(1)
        return level

    def save_level(self, path):
        """Safe a level to file currently not working
        :param path: patth for the file
        """
        with open(path, "w") as fp:
            for y in range(self.height):
                fp.write("".join([f"{int(self.map_gird[y][x].tile_type)};{self.map_gird[y][x].surface_id} " for x in
                                  range(self.width)]) + "\n")

    def highlight(self, position: Tuple[int, int]):
        """
        Highlight or un highlight a tile on the map
        :param position: screen coordinates of the cell to highlight
        :return:
        """
        x, y = position
        x, y = Level._pixel_to_grid_coord(x, y, self.scale)
        self.map.grid[y][x].highlighted = False if self.map.grid[y][x].highlighted else True
        self.map._render_tile_from_grid((x, y))

    def update_stage(self):
        """
        Update the current level stage / wave to the next one
        :return:
        """
        self.stage += 1
        self.spawn_frequenz = 1 / (self.stage)
        for spawner in self.spawners:
            spawner.spawn(self.stage * 10)

    def check_on_wave(self):
        """
        check if the current wave if over
        :return:
        """
        self.wave_done = all([len(spawner.on_the_way) == 0 for spawner in self.spawners]) and all(
            [len(spawner.spawned) == 0 for spawner in self.spawners])

    def update(self, delta_time: float) -> None:
        """
        Update the level
        Update Level, Map, then all spawners of the level
        :param delta_time:
        :return:
        """
        if self.timer.finished and self.wave_done:
            self.update_stage()

        self.check_on_wave()

        if self.wave_done and self.timer.finished:
            self.timer.finished = False
            self.timer.duration = 10

        self.map.update(delta_time)
        for spawner in self.spawners:
            spawner.update_spawn(delta_time, self.spawn_frequenz)
            spawner.update(delta_time)
        self.timer.update(delta_time)

    def render(self, scale: float) -> None:
        """Render the level.
        :param scale: Scale factor
        """
        self.scale = scale
        self.map.render(scale)
        for spawner in self.spawners:
            spawner.render(scale)
        self.timer.render(scale)
        self.coins.render()
