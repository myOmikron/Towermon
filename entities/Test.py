from typing import Tuple

import pygame
from entities.navigation.Math.Vector2 import Vector2

import settings
from entities.Entity import EnemyFactory
from entities.EntitySpawner import EntitySpawner
from entities.navigation.AStar import AStar
from entities.navigation.NavMesh import Cell, NavMesh


class Test:
    """
    A Class to test the Enemy Spawn system and there pathing
    """

    def __init__(self, scale):
        self.start = (0, 0)
        self.end = (499, 499)
        self.nav_mesh = NavMesh(settings.LEVEL_WIDTH, settings.LEVEL_HEIGHT,
                                [[Cell(Vector2((x, y))) for x in range(settings.LEVEL_WIDTH)] for y in
                                 range(settings.LEVEL_HEIGHT)])
        self.current_path = None
        enemy_factory = EnemyFactory('player.png', scale)
        self.spawner = EntitySpawner(dead=[], on_the_way=[], spawned=[], path=self.current_path,
                                     position=Vector2(self.start),
                                     factory=enemy_factory)

    def set_start(self, x: int, y: int, scale: float):
        """
        Set a start point for the enemy path and the position of the Spawner
        :param x: pixel coord
        :param y: pixel coord
        :param scale: current map scale
        :return: None
        """
        self.start = self._pixel_to_grid_coord(x, y, scale)
        self.spawner.position = Vector2(self.start)
        print(f"Set new Start position: {self.start}")

    def set_end(self, x, y, scale):
        """
        set the Target position of the enemy path
        :param x: pixel coord
        :param y: pixel coord
        :param scale: current map scale
        :return: None
        """
        self.end = self._pixel_to_grid_coord(x, y, scale)
        print(f"Set new End position: {self.end}")

    def spawn(self):
        self.spawner.spawn(1)
        print("spawned Enemy")

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

    def search(self):
        """
        Search the shortest path between the start and end point
        :return: None
        """
        # TODO: Optimize grid so there is no need to reset it every time
        # Reset the grid so all cells are not visited
        if self.current_path is not None:
            for row in self.nav_mesh.grid:
                for cell in row:
                    cell.visited = False
        path = self.nav_mesh.find_path(Vector2(self.start), Vector2(self.end), AStar)
        print(f"Calculated Path: {path}")
        if path is not None:
            self.current_path = path
            self.spawner.path = path

    @staticmethod
    def _rect_from_point(point: Tuple[int, int], size: int) -> pygame.rect.Rect:
        """
        create a rectangle from the given point
        :param point: topleft coordinates of the rect
        :param size: width and height of the rect
        :return: a new Rect
        """
        return pygame.rect.Rect(point[0], point[1], size, size)

    def update(self, delta_time: float) -> None:
        """
        update the spawner and spawn update
        :param delta_time: float
        :return: None
        """
        self.spawner.update(delta_time)
        self.spawner.update_spawn(delta_time, 1.0)

    def render(self, scale: float) -> None:
        """
        Render the path, startpoint, endpoint and then call the spawner render method the render all spawned entities
        :param scale: current map scale
        :return: None
        """
        if self.current_path:
            scaled_tile_size = round(settings.TILE_SIZE * scale)
            path = [(vec.x * scaled_tile_size, vec.y * scaled_tile_size) for vec in
                    self.current_path]
            s = pygame.display.get_surface()

            pygame.draw.rect(s, (0, 255, 0), self._rect_from_point(self._grid_to_pixel_coord(*self.start, scale=scale),
                                                                   scaled_tile_size), 1)
            pygame.draw.rect(s, (0, 0, 255),
                             self._rect_from_point(self._grid_to_pixel_coord(*self.end, scale=scale), scaled_tile_size),
                             1)
            pygame.draw.lines(s, (255, 0, 0), False, path, width=3)
        self.spawner.render(scale)
