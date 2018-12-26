from copy import deepcopy
from itertools import product


def simulate(grid, rounds=18, periodicity=1):
    n, m = len(grid), len(grid[0])
    tree_count, lumber_count = 0, 0
    eventual_count = 0
    for curr_round in range(rounds):
        # print(curr_round)
        # print('\n'.join([''.join(row) for row in grid]))
        next_grid = deepcopy(grid)
        for x in range(n):
            for y in range(m):
                tile = grid[x][y]
                tree_count, lumber_count = 0, 0
                for nx in range(x - 1, x + 2):
                    for ny in range(y - 1, y + 2):
                        if (nx == x and ny == y) or not 0 <= nx < n or not 0 <= ny < m:
                            continue

                        if grid[nx][ny] == "|":
                            tree_count += 1
                        elif grid[nx][ny] == "#":
                            lumber_count += 1
                if tile == "." and tree_count >= 3:
                    next_grid[x][y] = "|"
                elif tile == "|" and lumber_count >= 3:
                    next_grid[x][y] = "#"
                elif tile == "#" and (tree_count == 0 or lumber_count == 0):
                    next_grid[x][y] = "."
        grid = next_grid
        lumber_count = sum(
            1 for x, y in product(range(n), range(m)) if grid[x][y] == "#"
        )
        tree_count = sum(1 for x, y in product(range(n), range(m)) if grid[x][y] == "|")
        if (curr_round + 1) % periodicity == 1000000000 % periodicity:
            eventual_count = lumber_count * tree_count
    return lumber_count * tree_count, eventual_count


if __name__ == "__main__":
    with open("18.txt") as f:
        data = f.read().strip().split("\n")

    grid = [list(row) for row in data]
    part1, _ = simulate(grid)
    print("Part 1: {}".format(part1))
    _, part2 = simulate(grid, rounds=1000, periodicity=84)
    print("Part 2: {}".format(part2))
