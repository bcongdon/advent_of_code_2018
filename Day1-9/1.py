import itertools


def part_1(inputs):
    return sum(int(i) for i in inputs)


def part_2(inputs):
    acc = 0
    mem = {}
    for i in itertools.cycle(int(j) for j in inputs):
        acc += i
        if acc in mem:
            return acc
        mem[acc] = True


if __name__ == "__main__":
    with open("1.txt") as f:
        data = f.read().split()

    print(part_1(data))
    print(part_2(data))
