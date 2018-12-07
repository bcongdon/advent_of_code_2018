from collections import defaultdict

def part1(dependencies):
    dep_graph = defaultdict(set)
    for dep in dependencies:
        dep_graph[dep[0]]
        dep_graph[dep[1]].add(dep[0])

    order = []
    while len(dep_graph) > 0:
        can_be_executed = []
        for k, v in dep_graph.items():
            if len(v) == 0:
                can_be_executed.append(k)
        can_be_executed.sort()
        executing = can_be_executed[0]

        del dep_graph[executing]
        for k in dep_graph:
            dep_graph[k] -= set(executing)
        order.extend(executing)
    return ''.join(order)

def part2(dependencies):
    dep_graph = defaultdict(set)
    for dep in dependencies:
        dep_graph[dep[0]]
        dep_graph[dep[1]].add(dep[0])

    worker_cooldowns = [0] * 5
    worker_keys = [None] * 5
    time = 0
    order = []
    while len(dep_graph) > 0:
        for idx, w in enumerate(worker_cooldowns):
            if w != 0 or worker_keys[idx] is None:
                continue
            for k in dep_graph:
                dep_graph[k] -= set(worker_keys[idx])
            worker_keys[idx] = None

        can_be_executed = []
        for k, v in dep_graph.items():
            if len(v) == 0:
                can_be_executed.append(k)
        can_be_executed.sort()
        can_be_executed = can_be_executed[::-1]

        for idx, w in enumerate(worker_cooldowns):
            if w != 0 or not can_be_executed:
                continue
            executing = can_be_executed.pop()
            worker_cooldowns[idx] = 60 + ord(executing) - ord('A') + 1
            worker_keys[idx] = executing

            del dep_graph[executing]
            order.extend(executing)
        worker_cooldowns = [max(w - 1, 0) for w in worker_cooldowns]
        time += 1
    time += max(worker_cooldowns)

    return time

if __name__ == '__main__':
    with open('7.txt') as f:
        raw = f.readlines()

    dependencies = [(w[1], w[-3]) for w in [line.split(' ') for line in raw]]

    print('Part 1: {}'.format(part1(dependencies)))
    print('Part 2: {}'.format(part2(dependencies)))
