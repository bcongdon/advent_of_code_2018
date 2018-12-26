import numpy as np


def calculate(lines):
    guards = {}
    current_guard = None
    current_events = []
    for line in lines:
        date, content = line.split('] ')
        minute = int(date[-2:])

        if 'Guard' in content:
            if current_guard is not None:
                if current_guard not in guards:
                    guards[current_guard] = np.zeros(60)
                for sleep, awake in zip(current_events[::2], current_events[1::2]):
                    guards[current_guard][sleep:awake] += 1
            current_guard = int(content.split(' ')[1][1:])
            current_events = []
        elif 'falls' in content or 'wakes' in content:
            current_events.append(minute)

    max_guard_id, guard_schedule = max(
        guards.items(), key=lambda kv: kv[1].sum())
    part1 = max_guard_id * guard_schedule.argmax()

    max_minutes_asleep = max(minutes.max()
                             for guard_id, minutes in guards.items())
    max_guard_id, minute_asleep = next(
        (guard_id, minutes.argmax()) for guard_id, minutes in guards.items() if minutes.max() == max_minutes_asleep)
    part2 = max_guard_id * minute_asleep
    return part1, part2


if __name__ == '__main__':
    with open('4.txt') as f:
        lines = f.readlines()

    part1, part2 = calculate(lines)
    print("Part 1: {}".format(part1))
    print("Part 2: {}".format(part2))
