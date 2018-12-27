def parse_tree(data):
    num_children, num_metadata = data[:2]
    data = data[2:]

    total = 0
    child_values = []
    for _ in range(num_children):
        partial_total, value, data = parse_tree(data)
        child_values.append(value)
        total += partial_total

    value = 0
    if num_children == 0:
        value = sum(data[:num_metadata])
    else:
        value = sum(
            child_values[i - 1]
            for i in data[:num_metadata]
            if 0 <= (i - 1) < len(child_values)
        )

    return sum(data[:num_metadata]) + total, value, data[num_metadata:]


if __name__ == "__main__":
    with open("8.txt") as f:
        data = [int(i) for i in f.read().strip().split()]

    part1, part2, _ = parse_tree(data)
    print("Part 1: {}".format(part1))
    print("Part 2: {}".format(part2))
