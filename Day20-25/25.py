from collections import defaultdict


def dist(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))


def part1(points):
    edges = defaultdict(set)
    for i1, p1 in enumerate(points):
        for i2 in range(i1 + 1, len(points)):
            p2 = points[i2]
            if dist(p1, p2) <= 3:
                edges[i1].add(i2)
                edges[i2].add(i1)

    chosen = set()
    constellations = 0
    for p_idx, point in enumerate(points):
        if p_idx in chosen:
            continue

        constellations += 1
        frontier = [p_idx]
        while frontier:
            exploring = frontier.pop()
            chosen.add(exploring)
            for n in edges[exploring]:
                if n not in chosen and n not in frontier:
                    frontier.append(n)
    return constellations


if __name__ == "__main__":
    with open("25.txt") as f:
        points = f.read().strip().split("\n")

    points = [tuple(int(c) for c in p.split(",")) for p in points]

    print("Part 1: {}".format(part1(points)))
