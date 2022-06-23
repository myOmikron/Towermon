from NavMesh import NavMesh, Cell
from entities.navigation.AStar import AStar

from hypothesis import given, strategies as st
import random


def get_random_point(size: int):
    return random.randrange(0, size), random.randrange(0, size)


@given(st.integers(10, 100), st.floats(0.0, 0.8))
def test_generate_random_grid(size: int, block: float):
    grid = []
    print(block)
    for h in range(size):
        row = []
        for w in range(size):
            if random.random() <= block:
                row.append(Cell((w, h), passable=False))
            else:
                row.append(Cell((w, h)))
        grid.append(row)

    mesh = NavMesh(size, size, grid)
    print(mesh.print_grid())
    for i in range(100):
        start, end = get_random_point(size), get_random_point(size)
        if mesh.get_cell(start).passable and mesh.get_cell(end).passable:
            mesh.find_path(start, end, AStar)
            print(mesh.print_grid())
            break


@given(st.integers(10, 100))
def test_rais_condition(size: int):
    mesh = NavMesh(size, size, [])
    try:
        mesh.get_cell((-1, -1))
    except IndexError:
        print(f"caught index Error index: {-1, -1} dimension: {size, size}")
    try:
        mesh.get_cell((size+1, size+1))
    except IndexError:
        print(f"caught index Error index: {size+1, size+1} dimension: {size, size}")