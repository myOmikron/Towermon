import math
from dataclasses import field
from typing import List, Tuple, Any, Dict

from dataclasses import dataclass


@dataclass
class Cell:
    position: Tuple[int, int]
    visited: bool = False
    travel_cost: int = 0
    passable: bool = True

    def __hash__(self):
        return hash(self.position)


@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: Any = field(compare=False)


@dataclass
class NavMesh:
    width: int
    height: int
    grid: List[List[Cell]]
    paths: Dict[Tuple[Tuple[int, int], Tuple[int, int]], List[Cell]] = field(init=False, default_factory=lambda: dict())

    def get_cell(self, position: Tuple[int, int]) -> Cell:
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        raise IndexError(f"{x, y} <= 0 oder {x, y} > {self.width, self.height}")

    def get_neighbours(self, position):
        x, y = position
        for x_off, y_off in [(0, 1), (1, 0), (-1, 0), (0, -1)]:  # [(-1, 1), (1, -1), (1, 1), (-1, -1)]
            nx = x + x_off
            ny = y + y_off
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (cell := self.grid[ny][nx]).passable:
                    yield cell

    def print_grid(self):
        for row in self.grid:
            print("".join([str(x.travel_cost) if x.passable else 'X' for x in row]))

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int], solver, recalculate=False) -> List[Cell]:
        """
        Finds the sortest path between two points and caches it, if the path already exists it returns the cached
        version.
        :param recalculate: recalculate an existing path if True
        :param start: start point
        :param end: end point
        :param solver: search algorithm to find the path
        :return: the shortest path if possible
        """
        if not recalculate:
            if (path := self.paths.get((start, end))) is not None:
                return path

        def d(p1: Cell, p2: Cell) -> float:
            """
            Heuristic to estimate distance to goal
            :param p1: start point
            :param p2: end point
            :return: euclidian distance aka travel cost
            """
            x1, y1, = p1.position
            x2, y2 = p2.position
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        a = solver(d, lambda x, y: 1)
        path = a.search(self.get_cell(start), self.get_cell(end), self)
        self.paths[(start, end)] = path
        if path is not None:
            for cell in path:
                self.grid[cell.position[1]][cell.position[0]].travel_cost = 1
