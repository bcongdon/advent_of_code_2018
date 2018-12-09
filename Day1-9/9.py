from collections import deque

NUM_ELVES = 418
NUM_MARBLES = 70769


def simulate_game(players, marbles):
    circle = deque([0])
    scores = [0] * players
    for marble in range(1, marbles):
        curr_player = (marble - 1) % players
        if marble % 23 == 0:
            circle.rotate(7)
            removed = circle.pop()
            scores[curr_player] += marble + removed
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
    return max(scores)


if __name__ == '__main__':
    print("Part 1: {}".format(simulate_game(NUM_ELVES, NUM_MARBLES)))
    print("Part 2: {}".format(simulate_game(NUM_ELVES, NUM_MARBLES * 100)))
