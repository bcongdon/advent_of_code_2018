import numpy as np
import itertools
import networkx as nx

DEPTH = 9465
TARGET = (13, 704)

NEITHER = 0
TORCH = 1
CLIMBING = 2

ROCKY = 0
WET = 1
NARROW = 2


def make_grid(target):
    tx, ty = target

    grid = {}
    for x, y in itertools.product(range(tx + 1), range(ty + 1)):
        if (x, y) in ((0, 0), target):
            geo_idx = 0
        elif x == 0:
            geo_idx = y * 48271
        elif y == 0:
            geo_idx = x * 16807
        else:
            geo_idx = grid[(x - 1, y)][1] * grid[(x, y - 1)][1]
        ero = (geo_idx + DEPTH) % 20183
        risk = ero % 3
        grid[(x, y)] = (geo_idx, ero, risk)
    return grid


def part1(target):
    return sum(cell[2] for cell in make_grid(target).values())


def tool_is_valid(grid_type, tool):
    assert 0 <= grid_type < 3
    assert 0 <= tool < 3
    # Rocky needs either tool
    if grid_type == ROCKY:
        return tool != NEITHER

    # Wet needs climbing or neither
    if grid_type == WET:
        return tool != TORCH

    # Narrow needs neither or torch
    if grid_type == NARROW:
        return tool != CLIMBING
    raise 'Unknown grid type'


def part2(target):
    tx, ty = target
    buffer = 100
    grid = make_grid((tx + buffer, ty + buffer))
    G = nx.Graph()

    for x, y, t in itertools.product(range(tx + buffer), range(ty + buffer), range(3)):
        if not tool_is_valid(grid[(x, y)][2], t):
            continue

        for nt in range(3):
            if t != nt and tool_is_valid(grid[(x, y)][2], nt):
                G.add_edge((x, y, t), (x, y, nt), weight=7)

        for x_new, y_new in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if 0 <= x_new and 0 <= y_new:
                if not tool_is_valid(grid[(x_new, y_new)][2], t):
                    continue
                G.add_edge((x, y, t), (x_new, y_new, t), weight=1)

    return(nx.dijkstra_path_length(G, (0, 0, TORCH), (tx, ty, TORCH)))


if __name__ == "__main__":
    print("Part 1: {}".format(part1(TARGET)))
    print("Part 2: {}".format(part2(TARGET)))
