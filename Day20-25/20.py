# inspired by https://www.reddit.com/r/adventofcode/comments/a7uk3f/2018_day_20_solutions/ec61vb0/

from collections import defaultdict

directions = {"N": (1, 0), "S": (-1, 0), "E": (0, 1), "W": (0, -1)}


def maximum_doors(regex):
    x, y = 0, 0
    locations = []

    edges = defaultdict(set)
    distances = defaultdict(int)
    for char in regex:
        if char == "(":
            locations.append((x, y))
        elif char == ")":
            x, y = locations.pop()
        elif char == "|":
            x, y = locations[-1]
        else:
            dx, dy = directions[char]
            prev_x, prev_y = x, y
            x, y = x + dx, y + dy
            edges[(x, y)].add((prev_x, prev_y))
            if (x, y) in distances:
                distances[(x, y)] = min(
                    distances[(x, y)], distances[(prev_x, prev_y)] + 1
                )
            else:
                distances[(x, y)] = distances[(prev_x, prev_y)] + 1
    return max(distances.values()), sum(1 for v in distances.values() if v >= 1000)


if __name__ == "__main__":
    with open("20.txt") as f:
        regex = f.read().strip()

    regex = regex[1:-1]  # remove ^ and &
    part1, part2 = maximum_doors(regex)
    print("Part 1: {}".format(part1))
    print("Part 2: {}".format(part2))
