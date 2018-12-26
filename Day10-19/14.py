SEED = 768071


def simulate(recipes=SEED):
    elf1, elf2 = 0, 1
    scores = "37"
    sequence = str(recipes)
    sequence_len = len(sequence)

    found = False
    while len(scores) < recipes + 10 or not found:
        if len(sequence) <= len(scores) and sequence in scores[-sequence_len - 1 :]:
            found = True
            break

        recipe_sum = int(scores[elf1]) + int(scores[elf2])
        scores += str(recipe_sum)
        elf1 = (elf1 + int(scores[elf1]) + 1) % len(scores)
        elf2 = (elf2 + int(scores[elf2]) + 1) % len(scores)

    return scores[recipes : recipes + 10], scores.index(sequence)


if __name__ == "__main__":
    part1, part2 = simulate()
    print("Part 1: {}".format(part1))
    print("Part 2: {}".format(part2))
