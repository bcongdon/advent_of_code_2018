import re

def parse_register(raw):
    register_regex = re.compile(r'\[.*\]')
    raw = register_regex.search(raw).group(0)
    raw = raw[1:-1] # remove brackets
    return [int(i) for i in raw.split(',')]

def op_i(op_func):
    def wrapped(reg, a, b, c):
        reg[c] = op_func(reg[a], b)
        return reg
    return wrapped

def op_r(op_func):
    def wrapped(reg, a, b, c):
        reg[c] = op_func(reg[a], reg[b])
        return reg
    return wrapped

def op_ir(op_func):
    def wrapped(reg, a, b, c):
        reg[c] = op_func(a, reg[b])
        return reg
    return wrapped



addr = op_r(lambda a, b: a + b)
mulr = op_r(lambda a, b: a * b)
banr = op_r(lambda a, b: a & b)
borr = op_r(lambda a, b: a | b)
setr = op_r(lambda a, b: a)
gtrr = op_r(lambda a, b: 1 if a > b else 0)
eqrr = op_r(lambda a, b: 1 if a == b else 0)

addi = op_i(lambda a, b: a + b)
muli = op_i(lambda a, b: a * b)
bani = op_i(lambda a, b: a & b)
bori = op_i(lambda a, b: a | b)
seti = op_ir(lambda a, b: a)
gtri = op_i(lambda a, b: 1 if a > b else 0)
eqri = op_i(lambda a, b: 1 if a == b else 0)

gtir = op_ir(lambda a, b: 1 if a > b else 0)
eqir = op_ir(lambda a, b: 1 if a == b else 0)

all_ops = [addr, mulr, banr, borr, setr, gtrr, eqrr, addi, muli, bani, bori, seti, gtri, eqri, gtir, eqir]


def observe_samples(samples):
    gt_3_instructions = 0
    opcode_mapping = {i: set(range(len(all_ops))) for i in range(len(all_ops))}
    for sample in [s.strip() for s in samples if s.strip()]:
        before, instruction, after = sample.strip().split('\n')
        before_reg, after_reg = parse_register(before), parse_register(after)

        op_code, a, b, c = instruction.split()
        op_code, a, b, c = int(op_code), int(a), int(b), int(c)

        possible_instructions = set()
        for idx, op in enumerate(all_ops):
            result = op(list(before_reg), a, b, c)
            if result == after_reg:
                possible_instructions.add(idx)
        opcode_mapping[op_code] = opcode_mapping[op_code].intersection(possible_instructions)
        if len(possible_instructions) >= 3:
            gt_3_instructions += 1

    final_opcode_map = {}
    while opcode_mapping:
        satisfied = [key for key, value in opcode_mapping.items() if len(value) == 1]
        for key in satisfied:
            final_value = list(opcode_mapping[key])[0]
            final_opcode_map[key] = final_value
            del opcode_mapping[key]
            for opcode in opcode_mapping:
                opcode_mapping[opcode] -= set([final_value])

    return gt_3_instructions, final_opcode_map

def run_vm(opcode_map, instructions):
    registers = [0, 0, 0, 0]
    for instruction in instructions:
        op_code, a, b, c = instruction.split()
        op_code, a, b, c = int(op_code), int(a), int(b), int(c)

        op_func = all_ops[opcode_map[op_code]]
        registers = op_func(registers, a, b, c)

    return registers[0]


if __name__ == '__main__':
    with open('16.txt') as f:
        data = f.read().strip().split('\n\n')

    observations = data[:-1]
    part1, opcode_map = observe_samples(observations)
    print("Part 1: {}".format(part1))

    part2 = run_vm(opcode_map, data[-1].strip().split('\n'))
    print("Part 2: {}".format(part2))

