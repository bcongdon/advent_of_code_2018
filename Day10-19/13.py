from copy import deepcopy

direction_map = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}

cart_map = {">": "-", "v": "|", "<": "-", "^": "|"}

left_turns = {">": "^", "v": ">", "<": "v", "^": "<"}

right_turns = {">": "v", "v": "<", "<": "^", "^": ">"}


def parse_map(raw):
    data = raw.split("\n")
    grid = []
    n = len(data)
    m = max(len(line) for line in data)
    for _ in range(n):
        grid.append([""] * m)

    carts = {}
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c in "<>^v":
                carts[(x, y)] = (c, 0)
                c = cart_map[c]
            grid[y][x] = c

    return grid, carts


def simulate(rail_map, carts):
    first_crash = None
    while True:
        # print_map = deepcopy(rail_map)
        # for cart_loc, cart_data in carts.items():
        #    x, y = cart_loc
        #    direction, _ = cart_data
        #    print_map[y][x] = direction
        # print('\n'.join(''.join(line) for line in print_map))

        sorted_locs = list(carts.keys())
        sorted_locs.sort(key=lambda pos: (pos[1], pos[0]))

        if len(sorted_locs) == 1:
            return first_crash, sorted_locs[0]

        for cart_loc in sorted_locs:
            if cart_loc not in carts:
                continue

            x, y = cart_loc
            direction, state = carts[cart_loc]
            old_direction = direction

            map_tile = rail_map[y][x]
            dx, dy = 0, 0
            if map_tile == "\\":
                direction = (
                    left_turns[direction]
                    if direction in "^v"
                    else right_turns[direction]
                )
            elif map_tile == "/":
                direction = (
                    right_turns[direction]
                    if direction in "^v"
                    else left_turns[direction]
                )
            elif map_tile == "+":
                if state == 0:
                    direction = left_turns[direction]
                elif state == 2:
                    direction = right_turns[direction]
                state = (state + 1) % 3
            dx, dy = direction_map[direction]

            del carts[(x, y)]
            oldx, oldy = x, y
            x, y = x + dx, y + dy
            if (x, y) in carts:
                del carts[(x, y)]
                if first_crash is None:
                    first_crash = (x, y)
            else:
                if rail_map[y][x] == " ":
                    print(direction, old_direction, map_tile, dx, dy)
                    return

                carts[(x, y)] = direction, state


if __name__ == "__main__":
    with open("13.txt") as f:
        raw = f.read()

    rail_map, carts = parse_map(raw)
    part1, part2 = simulate(rail_map, carts)
    print("Part 1: {}".format(part1))
    print("Part 2: {}".format(part2))
