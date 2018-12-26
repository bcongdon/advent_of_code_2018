import re
import numpy as np

LINE_REGEX = re.compile(r"position=<(.*?),(.*?)> velocity=<(.*?),(.*?)>")


def parse_line(line):
    match = LINE_REGEX.match(line)
    x = match.group(1)
    y = match.group(2)
    vx = match.group(3)
    vy = match.group(4)

    return (int(x), int(y), int(vx), int(vy))


def simulate(particles):
    pos = np.zeros((len(particles), 2), dtype="int")
    vel = np.zeros((len(particles), 2), dtype="int")

    for idx, p in enumerate(particles):
        x, y, vx, vy = p
        pos[idx, :] = np.array([x, y])
        vel[idx, :] = np.array([vx, vy])

    min_spread, min_spread_config, min_spread_time = 2 ** 100, None, 0
    for i in range(20000):
        pos += vel

        min_x, min_y = np.min(pos[:, 0]), np.min(pos[:, 1])
        max_x, max_y = np.max(pos[:, 0]), np.max(pos[:, 1])

        spread = abs(max_x - min_x) + abs(max_y - min_y)
        if spread < min_spread:
            min_spread_config = np.copy(pos)
            min_spread_time = i
        min_spread = min(spread, min_spread)

    min_x, min_y = np.min(min_spread_config[:, 0]), np.min(min_spread_config[:, 1])
    max_x, max_y = np.max(min_spread_config[:, 0]), np.max(min_spread_config[:, 1])
    field = np.zeros((max_x - min_x + 1, max_y - min_y + 1))
    for row in min_spread_config:
        x, y = row
        field[x - min_x, y - min_y] = 1

    for row in field.T:
        print("".join("*" if v == 1 else " " for v in row))
    print("Time for message to appear: {}".format(min_spread_time + 1))


if __name__ == "__main__":
    with open("10.txt") as f:
        lines = f.readlines()

    particles = [parse_line(l) for l in lines]
    simulate(particles)
