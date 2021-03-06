import networkx as nx

DEFAULT_HP = 200
DEFAULT_ATTACK = 3


def simulate(grid, part2=False, elf_attack=3):
    grid = [list(line.strip()) for line in grid]
    units = []
    for y, l in enumerate(grid):
        for x, c in enumerate(l):
            if c == 'G':
                units.append([c, x, y, DEFAULT_HP, DEFAULT_ATTACK])
            elif c == 'E':
                units.append([c, x, y, DEFAULT_HP, elf_attack])

    for rnd in range(500):
        print("=_-=" * 10)
        units = [u for u in units if u[3] > 0]
        units = sorted(units, key=lambda u: (u[2], u[1]))
        # print('\n'.join(str(u) for u in units))
        print("ROUND: {}; ELF ATTACK STRENGTH: {}".format(rnd, elf_attack))
        print('\n'.join([str(''.join(line)) for line in grid]))

        for unit in units:
            # print('---')
            # print("CONSIDERING UNIT:", unit)
            if unit[3] <= 0:
                continue
            other_units = [other for other in units if tuple(unit) !=
                           tuple(other) and unit[0] != other[0] and other[3] > 0]
            if not other_units:
                remaining_hp = sum(u[3] for u in units if u[3] > 0)
                return rnd * remaining_hp

            has_target_in_range = any(True for t in other_units if abs(
                unit[1] - t[1]) + abs(unit[2] - t[2]) == 1)
            if not has_target_in_range:
                # Find targets adjacent to other units
                targets = []
                for other_unit in other_units:
                    _, ox, oy, _, _ = other_unit
                    for tx, ty in [(ox, oy + 1), (ox, oy - 1), (ox + 1, oy), (ox - 1, oy)]:
                        if grid[ty][tx] == '.':
                            targets.append((tx, ty))

                # Create graph
                G = nx.Graph()
                G.add_node((unit[1], unit[2]))
                for y, l in enumerate(grid):
                    for x, c in enumerate(l):
                        if c != '.' and not (x, y) == (unit[1], unit[2]):
                            continue
                        for n_x, n_y in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                            if grid[n_y][n_x] == '.' or (n_x, n_y) == (unit[1], unit[2]):
                                G.add_edge((x, y), (n_x, n_y))

                # print("TARGETS", targets)
                targets = sorted(targets, key=lambda t: abs(
                    unit[1] - t[0]) + abs(unit[2] - t[1]))

                target_dists = []
                for target in targets:
                    try:
                        path_len = nx.shortest_path_length(
                            G, source=(unit[1], unit[2]), target=target)
                        target_dists.append((path_len, target))
                    except nx.exception.NetworkXNoPath:
                        pass
                    except nx.exception.NodeNotFound:
                        pass

                first_steps = []
                if target_dists:
                    target_dists = sorted(
                        target_dists, key=lambda td: (td[0], td[1][1], td[1][0]))
                    target = target_dists[0][1]
                    first_steps = set([path[1] for path in nx.all_shortest_paths(
                        G, source=(unit[1], unit[2]), target=target)])
                if first_steps:
                    # print("FIRST STEPS", first_steps)
                    first_step = sorted(list(first_steps),
                                        key=lambda s: (s[1], s[0]))[0]

                    # Move the piece
                    # print("MOVING", unit, first_step)
                    assert grid[first_step[1]][first_step[0]] == '.'
                    assert grid[unit[2]][unit[1]] == unit[0]
                    grid[unit[2]][unit[1]] = '.'
                    grid[first_step[1]][first_step[0]] = unit[0]
                    unit[1] = first_step[0]
                    unit[2] = first_step[1]

            in_range = [t for t in other_units if abs(
                unit[1] - t[1]) + abs(unit[2] - t[2]) == 1]
            # print("IN RANGE", unit, in_range)
            if in_range:
                least_hp = min(unit[3] for unit in in_range)
                target_unit = sorted(
                    [u for u in in_range if u[3] == least_hp], key=lambda t: (t[2], t[1]))[0]
                # print("ATTACK", unit, target_unit)
                assert target_unit[3] > 0
                target_unit[3] -= unit[4]
                if target_unit[3] <= 0:
                    grid[target_unit[2]][target_unit[1]] = '.'
                if target_unit[3] <= 0 and target_unit[0] == 'E' and part2:
                    return False


if __name__ == "__main__":
    with open('15.txt') as f:
        lines = f.readlines()

    part1 = simulate(lines)
    print("Part 1: {}".format(part1))

    attack_strength = 4
    while not simulate(lines, part2=True, elf_attack=attack_strength):
        attack_strength += 1
    print("Part 2: {}".format(
        simulate(lines, elf_attack=attack_strength)))
