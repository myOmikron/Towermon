from dataclasses import field, dataclass
from typing import List, Tuple, Any, Dict

import settings
from .Math.vector2 import Vector2


@dataclass(slots=True)
class Cell:
    position: Vector2
    visited: bool = False
    travel_cost: int = 0
    passable: bool = True

    def __hash__(self):
        return hash(self.position)


@dataclass(order=True, slots=True)
class PrioritizedItem:
    priority: float
    item: Any = field(compare=False)


@dataclass(slots=True)
class NavMesh:
    width: int
    height: int
    grid: List[List[Cell]]
    paths: Dict[Tuple[Vector2, Vector2], List[Cell]] = field(init=False, default_factory=lambda: dict())

    def get_cell(self, position: Vector2) -> Cell:
        if 0 <= position.x < self.width and 0 <= position.y < self.height:
            return self.grid[position.y][position.x]
        raise IndexError(f"{position.x, position.y} <= 0 oder {position.x, position.y} > {self.width, self.height}")

    def get_neighbours(self, position: Vector2):
        x, y = position.x, position.y
        for x_off, y_off in settings.NEIGHBOURS:
            nx = x + x_off
            ny = y + y_off
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (cell := self.grid[int(ny)][int(nx)]).passable:
                    yield cell

    def print_grid(self):
        for row in self.grid:
            print("".join([str(x.travel_cost) if x.passable else 'X' for x in row]))

    def find_path(self, start: Vector2, end: Vector2, solver, recalculate=False) -> List[Cell]:
        """Finds the sortest path between two points and caches it, if the path already exists it returns the cached
        version.

        :param recalculate: recalculate an existing path if True
        :param start: start point
        :param end: end point
        :param solver: search algorithm to find the path
        :return: the shortest path if possible
        """
        if not recalculate:
            if (path := self.paths.get((start, end))) is not None:
                print("Found Path in cache")
                return path

        def d(p1: Vector2, p2: Vector2) -> float:
            """Heuristic to estimate distance to goal

            :param p1: start point
            :param p2: end point
            :return: euclidian distance aka travel cost
            """
            return p1.distance(p2)

        a = solver(d, lambda x, y: 1)
        path = a.search(start, end, self)
        if path is not None:
            self.paths[(start, end)] = path
        return path
