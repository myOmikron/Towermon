from collections import defaultdict
from dataclasses import dataclass, field
from math import inf
from queue import PriorityQueue
from typing import Callable, Dict, DefaultDict, Optional, List

from entities.navigation.Math.vector2 import Vector2
from entities.navigation.nav_mesh import PrioritizedItem
from entities.tile import Tile


@dataclass(slots=False)
class AStar:
    # estimate the cost to gol
    cost_to_gol: Callable[[Vector2, Vector2], float]
    # calculate the cost to next Cell
    cot_to_next_cell: Callable[[Vector2, Vector2], float]
    visited: set[Tile] = field(default_factory=lambda: set())
    open_set: PriorityQueue = field(default_factory=lambda: PriorityQueue())
    came_from: Dict = field(default_factory=lambda: dict())
    g_score: DefaultDict[Vector2, float] = field(default_factory=lambda: defaultdict(lambda: inf))
    f_score: DefaultDict[Vector2, float] = field(default_factory=lambda: defaultdict(lambda: inf))

    def reverse_path(self, current):
        path = [current]
        while current in self.came_from.keys():
            current = self.came_from[current]
            path.insert(0, current)
        return path

    def search(self, start: Vector2, end: Vector2, mesh) -> Optional[List[Vector2]]:
        """search the shortest path from start to end

        :param start:
        :param end:
        :param mesh:
        :return: if shortest-path exists it returns it else None
        """
        self.open_set.put(PrioritizedItem(0.0, start))
        self.g_score[start] = 0
        self.f_score[start] = self.cost_to_gol(start, end)

        while not self.open_set.empty():
            current = self.open_set.get().item
            if current == end:
                return self.reverse_path(current)
            for neighbor in mesh.get_neighbours(current):
                tentative_g_score = self.g_score[current] + self.cot_to_next_cell(
                    current,
                    neighbor.position
                ) + neighbor.travel_cost
                if tentative_g_score < self.g_score[neighbor.position]:
                    self.came_from[neighbor.position] = current
                    self.g_score[neighbor.position] = tentative_g_score
                    self.f_score[neighbor.position] = tentative_g_score + self.cost_to_gol(neighbor.position,
                                                                                           end) + neighbor.travel_cost
                    if neighbor not in self.visited:
                        self.open_set.put(PrioritizedItem(self.f_score[neighbor.position], neighbor.position))
                        self.visited.add(neighbor)
        return None
