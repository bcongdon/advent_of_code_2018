# influenced by https://www.reddit.com/r/adventofcode/comments/a3kr4r/2018_day_6_solutions/eb7385m/

import itertools
from collections import defaultdict, Counter


def part1(points):
    max_x, max_y = max(x[0] for x in points), max(x[1] for x in points)

    grid = defaultdict(lambda: -1)
    for x, y in itertools.product(range(max_x + 1), range(max_y + 1)):
        closest_dist = min(abs(x - i) + abs(y - j) for i, j in points)
        closest_points = [
            (i, j) for i, j in points if abs(x - i) + abs(y - j) == closest_dist
        ]
        if len(closest_points) > 1:
            grid[x, y] = -1
        else:
            grid[x, y] = closest_points[0]

    # Exclude corners of grid
    infinite_points = (
        set(grid[(x, max_y - 1)] for x in range(max_x))
        .union((grid[(max_x - 1, y)] for y in range(max_y)))
        .union((grid[(x, 0)] for x in range(max_x)))
        .union((grid[(0, y)] for y in range(max_y)))
    )

    grid_values = list(grid.values())
    return max(grid_values.count(p) for p in points if p not in infinite_points)


def part2(points):
    max_x, max_y = max(x[0] for x in points), max(x[1] for x in points)

    return sum(
        1
        for x in range(max_x)
        for y in range(max_y)
        if sum(abs(x - i) + abs(y - j) for i, j in points) < 10000
    )


if __name__ == "__main__":
    with open("6.txt") as f:
        points = f.readlines()

    points = [tuple(int(i) for i in l.split(",")) for l in points]
    print("Part 1: {}".format(part1(points)))
    print("Part 2: {}".format(part2(points)))
