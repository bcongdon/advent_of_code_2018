from collections import defaultdict


def parse_rules(lines):
    rules = {}
    for l in lines:
        parts = l.split()
        rules[parts[0]] = parts[-1]
    return rules


def part1(initial_state, rules, generations=20):
    state = defaultdict(lambda: ".")
    for idx, val in enumerate(initial_state):
        state[idx] = val

    prev_sum = 0
    diffs = []
    for _ in range(generations):
        prev_state = state.copy()
        state = defaultdict(lambda: ".")
        start = min(prev_state.keys()) - 5
        end = max(prev_state.keys()) + 5
        for start_idx in range(start, end + 1):
            chunk = "".join([prev_state[i] for i in range(start_idx, start_idx + 5)])
            state[start_idx + 2] = rules.get(chunk, ".")
        curr_sum = sum(key for key, val in state.items() if val == "#")
        diffs.append(curr_sum - prev_sum)
        prev_sum = curr_sum

    avg_diff = sum(diffs[-100:]) // 100
    return sum(key for key, val in state.items() if val == "#"), avg_diff


def part2(initial_state, rules):
    iters = 1000
    curr_sum, diff = part1(initial_state, rules, iters)
    return (50000000000 - iters) * diff + curr_sum


if __name__ == "__main__":
    with open("12.txt") as f:
        raw = f.readlines()

    initial_state = raw[0].split()[-1]
    rules = parse_rules(raw[2:])

    print("Part 1: {}".format(part1(initial_state, rules)[0]))
    print("Part 2: {}".format(part2(initial_state, rules)))
