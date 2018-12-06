def part1(polymer):
    changed = True

    buf = []
    for c in polymer:
        if buf and buf[-1].lower() == c.lower() and buf[-1] != c:
            buf.pop()
        else:
            buf.append(c)

    return len(buf)

def part2(polymer):
    types = set(list(polymer.lower()))

    return min([part1(polymer.replace(t, '').replace(t.upper(), '')) for t in types])


if __name__ == '__main__':
    with open('5.txt') as f:
        polymer = f.read().replace('\n', '')

    print('Part 1: {}'.format(part1(polymer)))
    print('Part 2: {}'.format(part2(polymer)))
