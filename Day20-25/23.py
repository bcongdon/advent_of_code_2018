from z3 import *


def parse_row(row):
    pos_section, r_section = row.split(" ")
    numbers = pos_section[5:-2].split(",")
    x, y, z = [int(i) for i in numbers]
    r = int(r_section[2:])
    return (x, y, z, r)


def part1(bots):
    largest_range = max(r for _, _, _, r in bots)
    sx, sy, sz = next((x, y, z) for x, y, z, r in bots if r == largest_range)

    return sum(
        1
        for x, y, z, r in bots
        if abs(x - sx) + abs(y - sy) + abs(z - sz) <= largest_range
    )


def part2(bots):
    # Heavily influenced by https://www.reddit.com/r/adventofcode/comments/a8s17l/2018_day_23_solutions/ecdbux2/
    x, y, z = Int('x'), Int('y'), Int('z')

    def z3_abs(x):
        return If(x >= 0, x, -x)

    o = Optimize()

    bot_ranges = [
        Int('in_range_of_bot_' + str(i)) for i in range(len(bots))
    ]

    for i in range(len(bots)):
        nx, ny, nz, r = bots[i]
        # Add the constraint for each bot that the bot is in range iff the chosen
        # (x, y, y) is within `r` manhatten distance of the bot
        o.add(bot_ranges[i] == If(z3_abs(x - nx) +
                                  z3_abs(y - ny) + z3_abs(z - nz) <= r, 1, 0))

    range_count = Int('sum')
    o.add(range_count == sum(bot_ranges))

    dist_from_zero = Int('dist')
    o.add(dist_from_zero == z3_abs(x) + z3_abs(y) + z3_abs(z))

    # Maximize bots in range
    o.maximize(range_count)

    # Minimize distance of the center from zero
    h2 = o.minimize(dist_from_zero)
    o.check()

    # Return lowest distance from zero
    return o.lower(h2)


if __name__ == "__main__":
    with open("23.txt") as f:
        lines = f.read().strip().split("\n")

    bots = [parse_row(row) for row in lines]
    print("Part 1: {}".format(part1(bots)))
    print("Part 2: {}".format(part2(bots)))
