from collections import defaultdict
from dataclasses import dataclass, field
from math import inf
from queue import PriorityQueue
from typing import Callable, Dict, DefaultDict, Optional, List

from entities.navigation.NavMesh import Cell, PrioritizedItem


@dataclass
class AStar:
    # estimate the cost to gol
    cost_to_gol: Callable[[Cell, Cell], float]
    # calculate the cost to next Cell
    cot_to_next_cell: Callable[[Cell, Cell], float]
    open_set: PriorityQueue = field(default_factory=lambda: PriorityQueue())
    came_from: Dict = field(default_factory=lambda: dict())
    g_score: DefaultDict = field(default_factory=lambda: defaultdict(lambda: inf))
    f_score: DefaultDict = field(default_factory=lambda: defaultdict(lambda: inf))

    def reverse_path(self, current):
        path = [current]
        while current in self.came_from.keys():
            current = self.came_from[current]
            path.insert(0, current)
        return path

    def search(self, start: Cell, end: Cell, mesh) -> Optional[List[Cell]]:
        """
        search the shortest path from start to end
        :param start:
        :param end:
        :param mesh:
        :return: if shortest-path exists it returns it else None
        TODO: no PriorityQueue and no Cell in the Queue for a better performance ?
        """
        self.open_set.put(PrioritizedItem(0.0, start))
        self.g_score[start] = 0
        self.f_score[start] = self.cost_to_gol(start, end)

        while not self.open_set.empty():
            current = self.open_set.get().item
            if current == end:
                return self.reverse_path(current)
            for neighbor in mesh.get_neighbours(current.position):
                tentative_g_score = self.g_score[current] + self.cot_to_next_cell(current,
                                                                                  neighbor) + neighbor.travel_cost
                if tentative_g_score < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g_score
                    self.f_score[neighbor] = tentative_g_score + self.cost_to_gol(neighbor, end)
                    if not neighbor.visited:
                        neighbor.visited = True
                        self.open_set.put(PrioritizedItem(self.f_score[neighbor], neighbor))
        return None
