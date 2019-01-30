import numpy as np
import re

POS_REGEX = re.compile("(.)=(\d?.*), (.)=(\d?.*)\.\.(\d?.*)")


def simulate(grid, source_pos):
    to_process = [source_pos]
    # while to_process:
    i = 0
    while to_process:
        i += 1
        x, y = to_process.pop()
        # print((x, y), to_process)
        # print(print_grid(grid))
        # print('-' * 50)
        # print('\n')
        c = grid[x, y]
        modified = []
        if c == '|':
            # Put another '|' below if the space is empty
            if y + 1 < grid.shape[1] and grid[x, y + 1] == '.':
                grid[x, y + 1] = '|'
                modified.append((x, y + 1))
            elif y + 1 < grid.shape[1]:
                supported = True
                # Check left
                for nx in range(x, -1, -1):
                    if grid[nx, y + 1] == '.':
                        supported = False
                        break
                    if grid[nx, y] == '#':
                        break
                else:
                    supported = False
                # Check right
                for nx in range(x, grid.shape[0]):
                    if grid[nx, y + 1] == '.':
                        supported = False
                        break
                    if grid[nx, y] == '#':
                        break
                else:
                    supported = False
                if supported:
                    grid[x, y] = '~'
                    modified.append((x, y))

        if c == '~':
            for nx, ny in [(x + 1, y), (x - 1, y)]:
                if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] not in ('~', '#'):
                    grid[nx, ny] = '~'
                    modified.append((nx, ny))

        if c == '|' and y + 1 < grid.shape[1] and grid[x, y + 1] in ('~', '#'):
            for nx, ny in [(x - 1, y), (x + 1, y)]:
                if 0 <= nx < grid.shape[0] and grid[nx, y] == '.':
                    grid[nx, y] = '|'
                    modified.append((nx, y))

        for mx, my in modified:
            for nx, ny in [(mx + 1, my), (mx - 1, my), (mx, my + 1), (mx, my - 1), (mx, my)]:
                if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
                    to_process.append((nx, ny))
    print(print_grid(grid))
    with open("17-out.txt", 'w+') as f:
        f.write(print_grid(grid))

    still, flowing = np.count_nonzero(
        grid == '~'), np.count_nonzero(grid == '|')
    return still + flowing, still


def make_grid(positions):
    raw_parsed = []
    for line in positions:
        match = POS_REGEX.match(line)
        c1, v1, c2, v2, v3 = match.groups()
        v1, v2, v3 = int(v1), int(v2), int(v3)
        raw_parsed.append((c1, v1, c2, v2, v3))

    min_x, min_y, max_x, max_y = 2**100, 2**100, -2**100, -2**100
    for c1, v1, c2, v2, v3 in raw_parsed:
        if c1 == 'x':
            min_x = min(min_x, v1)
            max_x = max(max_x, v1)
            min_y = min(min_y, v2, v3)
            max_y = max(max_y, v2, v3)
        else:
            min_x = min(min_x, v2, v3)
            max_x = max(max_x, v2, v3)
            min_y = min(min_y, v1)
            max_y = max(max_y, v1)
    min_x -= 10
    max_x += 10
    grid = np.full((max_x - min_x, max_y - min_y + 1), '.', dtype=str)
    for c1, v1, c2, v2, v3 in raw_parsed:
        if c1 == 'x':
            x = v1 - min_x
            y1 = v2 - min_y
            y2 = v3 - min_y
            grid[x, y1:y2 + 1] = '#'
        else:
            y = v1 - min_y
            x1 = v2 - min_x
            x2 = v3 - min_x
            grid[x1:x2 + 1, y] = '#'
    grid[500 - min_x, 0] = '|'
    return grid, (500 - min_x, 0)


def print_grid(grid):
    out = '\n'.join(''.join(row) for row in grid.T)
    return out


if __name__ == "__main__":
    with open('17.txt') as f:
        lines = f.readlines()

    grid, source_pos = make_grid(lines)

    part1, part2 = simulate(grid, source_pos)
    print("Part 1: {}".format(part1))
    print("Part 2: {}".format(part2))
