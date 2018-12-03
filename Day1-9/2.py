from collections import Counter

def part1(lines):
    count_2 = 0
    count_3 = 0
    for line in lines:
        counts = Counter(list(line)).items()
        if any(c[1] == 2 for c in counts):
            count_2 += 1
        if any(c[1] == 3 for c in counts):
            count_3 += 1

    return count_2 * count_3

def part2(lines):
    for i, l1 in enumerate(lines):
        for j in range(i+1, len(lines)):
            l2 = lines[j]
            chars = zip(list(l1), list(l2))
            off_count = sum(1 for (a, b) in chars if a != b)
            if off_count == 1:
                return ''.join([a for (a, b) in chars if a == b])


if __name__ == '__main__':
    with open("2.txt") as f:
        data = f.read().split()
    
    part1_result = part1(data)
    print("Part 1: {}".format(part1_result))

    part2_result = part2(data)
    print("Part 2: {}".format(part2_result))
