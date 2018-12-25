import re
from recordtype import recordtype
from copy import deepcopy

Group = recordtype('Group', ['team', 'units', 'hp', 'immunities',
                             'weaknesses', 'damage', 'damage_type', 'initiative', 'id'])

weakness_re = re.compile(r'weak to (.*?)(;|\))')
immunity_re = re.compile(r'immune to (.*?)(;|\))')
damage_re = re.compile(r'does (\d+) (\w+) damage')


def parse_group(team, group, _id):
    group = group.strip()
    words = group.split()
    units = int(words[0])
    hp = int(words[4])

    immunities, weaknesses = [], []
    if 'immune to' in group:
        matches = immunity_re.search(group)
        immunities = matches.group(1).replace(' ', '').split(',')

    if 'weak to' in group:
        matches = weakness_re.search(group)
        weaknesses = matches.group(1).replace(' ', '').split(',')

    matches = damage_re.search(group)
    damage = int(matches.group(1))
    damage_type = matches.group(2).strip()
    initiative = int(words[-1])

    return Group(team, units, hp, immunities, weaknesses, damage, damage_type, initiative, _id)


def damage_possible(group1, group2):
    if group1.damage_type in group2.immunities:
        return 0

    total_damage = group1.units * group1.damage
    if group1.damage_type in group2.weaknesses:
        total_damage *= 2
    return total_damage


def hash_group(group):
    return "{}-{}".format(group.team, group.id)


def simulate(groups, boost=0):
    for group in groups:
        if group.team == 'immunity':
            group.damage += boost

    while len(set(g.team for g in groups)) == 2:
        groups.sort(key=lambda g: (
            (g.units * g.damage), g.initiative), reverse=True)

        pairings = []
        selected = set()
        for attacker in groups:
            targets = [g for g in groups if hash_group(
                g) not in selected and g.team != attacker.team and damage_possible(attacker, g) > 0]
            if not targets:
                continue
            target = sorted(targets, key=lambda g: (-damage_possible(
                attacker, g), -(g.units * g.damage), -g.initiative))[0]
            # targets.remove(target)
            selected.add(hash_group(target))
            pairings.append((attacker, target))

        pairings.sort(key=lambda p: p[0].initiative, reverse=True)
        stalemate = True
        for attacker, defender in pairings:
            damage = damage_possible(attacker, defender)
            units_killed = min(defender.units, damage // defender.hp)
            if units_killed > 0:
                stalemate = False
            defender.units -= units_killed

        if stalemate:
            raise Exception("Stalemate")

        groups = [g for g in groups if g.units > 0]
    return sum(g.units for g in groups), groups[0].team


if __name__ == '__main__':
    with open('24.txt') as f:
        immune, infection = f.read().strip().split('\n\n')

    immune, infection = immune.split('\n')[1:], infection.split('\n')[1:]

    immune = [parse_group('immunity', group, idx + 1)
              for idx, group in enumerate(immune)]
    infection = [parse_group('infection', group, idx + 1)
                 for idx, group in enumerate(infection)]

    part1, _ = simulate(deepcopy(immune + infection))
    print("Part 1: {}".format(part1))

    boost = 0
    while True:
        boost += 1
        try:
            part2, team = simulate(deepcopy(immune + infection), boost)
            if team == 'immunity':
                print("Part 2: {}".format(part2))
                break
        except Exception:
            pass
