import math
import random
from typing import Tuple, List, Union

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
from entities.ui.button import ButtonGrid, Button, generate_all_buttons
from entities.ui.health_bar import HealthBar
from entities.ui.hud import HUD
from entities.ui.wallet import Wallet
from utils import image
from json_utils import json_parser
from entities.pokemon_tower import PokemonTower, Projectile


def generate_map(name, width, height):
    with open(name, "w") as fp:
        for h in range(height):
            for w in range(width):
                if random.random() >= 0.5:
                    fp.write(" 1;1")
                else:
                    fp.write(" 0;0")
            fp.write("\n")


class Map:
    width: int
    height: int
    scale: float
    game_screen: SurfaceType
    map_screen: Surface
    grid: NDArray[NDArray[Tile]]
    towers: dict
    tiles: NDArray[Surface]
    spawns: List[Vector2]
    target: Vector2
    high_light: Surface
    pokemon_imgs: dict
    """Map for the Level"""

    def __init__(self, width, height, game_screen, grid, tiles, spawns, target):
        self.width = width
        self.height = height
        self.scale = 0.9
        self.game_screen = game_screen
        self.map_screen = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT - settings.UI_HEIGHT))
        self.grid = grid
        self.towers = dict()
        self.tiles = tiles
        self.spawns = spawns
        self.target = target
        self.high_light = utils.image.load_png("highlight.png")
        self.pokemon_imgs = self.load_imgs()
        self.offset = (0, 0)

    def add_tile(self, tile: Tile, position: Vector2):
        """
        Add a tile to the given position on the map_grid
        :param tile: tile you want to add
        :param position: game world coordinates of the tile
        :return:
        """
        self.grid[position.y][position.x] = tile
        self._render_tile_from_grid((int(position.x), int(position.y)))

    @staticmethod
    def load_imgs():
        img_dict = dict()
        for pokemon in json_parser.get_pokemon_list():
            img_dict[pokemon] = utils.image.load_png(pokemon + '.png')
        return img_dict

    def _render_tower(self, position: Tuple[int, int]):
        tower = self.towers[position]
        img = self.pokemon_imgs[tower.name]
        self._render_tile(img, position)

    def _render_tile_from_grid(self, position: Tuple[int, int], offset: Tuple[int, int]):
        x, y = position
        tile = self.grid[y + offset[1]][x + offset[0]]
        self._render_tile(self.tiles[tile.surface_id], position)
        if position in self.towers.keys():
            self._render_tower((x, y))
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
        screen_height = screen_height - settings.UI_HEIGHT

        num_x = math.ceil(screen_width / scaled_tile_size)
        num_y = math.ceil(screen_height / scaled_tile_size)
        return num_x, num_y

    def _render(self, scale: float, offset: Tuple[int, int], trigger_rerender) -> None:
        """Trigger a complete rerender."""
        if self.scale != scale or self.offset != offset or trigger_rerender:
            self.scale = scale
            self.offset = offset
            num_x, num_y = self._calc_visible_tiles()
            self.map_screen.fill((68, 167, 169))
            for y in range(0, num_y + 2):
                for x in range(0, num_x + 2):
                    if y < self.height and x < self.width:
                        self._render_tile_from_grid((x, y), offset)
                        if (x + offset[0], y + offset[1]) in self.towers.keys():
                            self._render_tower((x + offset[0], y + offset[1]))

    def update(self, delta_time: float) -> None:
        ...

    def render(self, scale: float, offset: Tuple[int, int], trigger_rerender: bool) -> None:
        """Render the level.
        :param trigger_rerender: Force rerender
        :param scale: Scale factor
        :param offset: Offset to apply
        """
        self._render(scale, offset, trigger_rerender)
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
            time = str(f"{self.duration:.0f}")
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
    wallet: Wallet
    wave_done: bool
    spawn_frequenz: float = 1
    stage: int = 0
    health_bar: HealthBar
    game_over: bool
    ui: ButtonGrid
    current_selection: Union[Tuple[int, int], None]
    game_screen: SurfaceType
    nav_mesh: NavMesh
    bullets: [Projectile]

    def __init__(self, width: int, height: int, game_screen: SurfaceType, map: Map, *groups: AbstractGroup):
        self.scale = 0.9
        self.current_selection = None
        self.map = map
        self.target = map.target
        self.wave_done = False
        self.game_over = False
        self.game_screen = game_screen
        self.bullets = []

        buttons = [Button(background, highlight) for background, highlight in generate_all_buttons()]

        # self.health_bar = HealthBar(200, 20, 100, (settings.SCREEN_WIDTH - 250, 50))
        self.hud = HUD(game_screen, (settings.SCREEN_WIDTH - 448, 10))

        self.ui = ButtonGrid(settings.SCREEN_WIDTH, settings.UI_HEIGHT,
                             (0, settings.SCREEN_HEIGHT - settings.UI_HEIGHT), buttons, game_screen)

        enemy_factory = EnemyFactory(1)
        self.nav_mesh = NavMesh(width, height, map.grid)

        paths = [self.nav_mesh.find_path(spawn, map.target, AStar) for spawn in map.spawns]

        self.spawners = [EnemySpawner(
            dead=[],
            on_the_way=[],
            spawned=[],
            path=path,
            position=spawn,
            factory=enemy_factory,
            last_delta=0, health_callback=self.hud.update_health)
            for spawn, path in zip(map.spawns, paths)]

    def start(self, screen):
        """
        Start the level
        :param screen: game screen
        :return:
        """
        self.timer = Timer(settings.TIMER, Vector2(((settings.SCREEN_WIDTH // 2) - 100, 10)), screen)
        self.wallet = Wallet(settings.COINS, screen)
        self.hud.update_coins(self.wallet.coins)

    def render_path(self, path, scale):
        """
        Render a path from a spawner for debug only
        :param path:
        :param scale:
        :return:
        """
        pygame.draw.lines(self.game_screen, (0, 0, 0), False,
                          [(int(cell.x * settings.TILE_SIZE * scale), int(cell.y * settings.TILE_SIZE * scale)) for cell
                           in path])

    def _check_path(self, position: Tuple[int, int]):
        """
        check if the current position is intersecting with a path, if there is an intersection, we try to calculate a
        new path, if there is a new possible path you can build there
        :param position:
        :return:
        """
        for spawner in self.spawners:
            if position in [(c.x, c.y) for c in spawner.path]:
                self.map.grid[position[1]][position[0]].passable = False
                new_path = self.nav_mesh.find_path(spawner.position, self.target, AStar, recalculate=True)
                self.map.grid[position[1]][position[0]].passable = True
                if new_path is None:
                    return False
                else:
                    spawner.path = new_path
        return True

    def build_tower(self, tower: PokemonTower, position: Tuple[int, int]):
        x, y = position
        if tower.cost <= self.wallet.coins and not self.timer.finished and self.map.grid[y][
            x].tile_type != TileType.BLOCKED:
            if self._check_path(position):
                self.wallet.coins -= tower.cost
                self.hud.update_coins(self.wallet.coins)
                self.map.towers[position] = tower
                self.map.grid[y][x].tile_type = TileType.TURRET
                self.map.grid[y][x].passable = False

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

        map = Map(grid.shape[1], grid.shape[0], pygame.display.get_surface(), grid, tiles, spawns, target)

        level = Level(grid.shape[1], grid.shape[0], pygame.display.get_surface(), map)

        # images = utils.image.load_tile_map("trainer_TEAMROCKET_M.png", (32, 48))
        # enemy_factory = EnemyFactory(1)
        # nav_mesh = NavMesh(grid.shape[1], grid.shape[0], grid)

        # paths = [nav_mesh.find_path(spawn, target, AStar) for spawn in spawns]

        # level.spawns = [
        #    EnemySpawner(dead=[], on_the_way=[], spawned=[], path=path, position=spawn, factory=enemy_factory,
        #                 last_delta=0, health_callback=None) for spawn, path in zip(spawns, paths)]

        # level.target = target
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

    def highlight(self, position: Tuple[int, int], offset: Tuple[int, int]):
        """
        Highlight or un highlight a tile on the map
        :param offset: Offset of the camera
        :param position: screen coordinates of the cell to highlight
        :return:
        """
        x, y = position
        if 0 <= x <= settings.SCREEN_WIDTH and 0 <= y <= settings.SCREEN_HEIGHT - settings.UI_HEIGHT:
            x, y = Level._pixel_to_grid_coord(x, y, self.scale)
            x, y = x + offset[0], y + offset[1]
            if x < self.map.width and y < self.map.height:
                if self.current_selection is not None:
                    if self.current_selection == (x, y):
                        self.map.grid[y][x].highlighted = not self.map.grid[y][x].highlighted
                        self.current_selection = None
                    else:
                        self.map.grid[self.current_selection[1]][self.current_selection[0]].highlighted = not \
                            self.map.grid[self.current_selection[1]][self.current_selection[0]].highlighted
                        self.map.grid[y][x].highlighted = not self.map.grid[y][x].highlighted
                        self.current_selection = (x, y)
                else:
                    self.map.grid[y][x].highlighted = not self.map.grid[y][x].highlighted
                    self.current_selection = (x, y)
                if self.current_selection is not None and self.ui.current_selection is not None:
                    # place tower
                    self.map.grid[y][x].highlighted = not self.map.grid[y][x].highlighted
                    self.current_selection = None
                    self.build_tower(
                        PokemonTower(json_parser.get_pokemon_list()[self.ui.current_selection], x, y), (x, y)
                    )
            return
        self.ui.click(position)

    def update_stage(self):
        """
        Update the current level stage / wave to the next one
        :return:
        """
        self.stage += 1
        self.spawn_frequenz = 1 / self.stage
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

        # if not self.health_bar.alive:
        #    self.game_over = True

        if self.timer.finished and self.wave_done:
            self.update_stage()

        self.check_on_wave()

        if self.wave_done and self.timer.finished:
            self.timer.finished = False
            self.timer.duration = settings.TIMER

        self.map.update(delta_time)

        for spawner in self.spawners:
            spawner.update_spawn(delta_time, self.spawn_frequenz)
            spawner.update(delta_time)
            for pokemon in self.map.towers.values():
                pokemon.deactivate()
                for spawner in self.spawners:
                    for enemy in spawner.on_the_way:
                        if pokemon.attack(enemy) == True:
                            # Get Pixel coordinates
                            enemy_pos = self._grid_to_pixel_coord(enemy.position.x, enemy.position.y, self.scale)
                            pos = self._grid_to_pixel_coord(pokemon.x, pokemon.y, self.scale)
                            # create Projectile
                            bullet = Projectile(pos, enemy_pos, enemy)
                            self.bullets.append(bullet)
                            # calculate coins
                            if enemy.life <= 0:
                                self.wallet.coins += 50
                                print(enemy.type + str(enemy.life))
        self.timer.update(delta_time)

    def render(self, scale: float, offset: Tuple[int, int], trigger_rerender: bool) -> None:
        """Render the level.
        :param trigger_rerender: Force a rerender
        :param offset: Offset to apply
        :param scale: Scale factor
        """
        self.scale = scale
        self.map.render(scale, offset, trigger_rerender)
        for pokemon in self.map.towers.values():
            if pokemon.is_active():
                self.render_attack(pokemon)
        self.render_bullets()
        for spawner in self.spawners:
            spawner.render(scale)
            # self.render_path(spawner.path, scale)
        self.timer.render(scale)
        # self.health_bar.render(1)
        self.hud.update_coins(self.wallet.coins)
        self.hud.render(1)
        self.ui.render()

    def render_bullets(self):
        for bullet in self.bullets:
            if len(bullet.path) == 0:
                self.bullets.remove(bullet)
            else:
                i = 0
                while len(bullet.path) > 0 and (i < 2):
                    bullet.render(self.game_screen)
                    bullet.move()
                    i += 1

    def render_attack(self, pokemon: PokemonTower):
        pixel_pos = self._grid_to_pixel_coord(pokemon.x, pokemon.y, self.scale)
        # pos_x = (pixel_pos[0]) - self.scale * pokemon.range * settings.TILE_SIZE
        # pos_y = (pixel_pos[1]) - self.scale * pokemon.range * settings.TILE_SIZE
        # side = ((pokemon.range*2)+1) * self.scale * settings.TILE_SIZE
        pos_x = pixel_pos[0] - 2
        pos_y = pixel_pos[1] - 2
        side = self.scale * settings.TILE_SIZE + 4
        surface = Surface((side, side))
        surface.fill((0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        rect = pygame.Rect(0, 0, side, side)
        pygame.draw.rect(surface, pygame.Color(255, 0, 0), rect, width=2)
        self.game_screen.blit(surface, (pos_x, pos_y))
