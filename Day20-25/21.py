import re


def parse_register(raw):
    register_regex = re.compile(r"\[.*\]")
    raw = register_regex.search(raw).group(0)
    raw = raw[1:-1]  # remove brackets
    return [int(i) for i in raw.split(",")]


def op_i(op_func):
    def wrapped(reg, a, b, c):
        reg[c] = op_func(reg[a], b)
        return reg

    return wrapped


def op_r(op_func):
    def wrapped(reg, a, b, c):
        b_val = reg[b] if b < len(reg) else 0
        reg[c] = op_func(reg[a], b_val)
        return reg

    return wrapped


def op_ir(op_func):
    def wrapped(reg, a, b, c):
        b_val = reg[b] if b < len(reg) else 0
        reg[c] = op_func(a, b_val)
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

ops_list = [
    addr,
    mulr,
    banr,
    borr,
    setr,
    gtrr,
    eqrr,
    addi,
    muli,
    bani,
    bori,
    seti,
    gtri,
    eqri,
    gtir,
    eqir,
]

ops_dict = {
    "addr": addr,
    "mulr": mulr,
    "banr": banr,
    "borr": borr,
    "setr": setr,
    "gtrr": gtrr,
    "eqrr": eqrr,
    "addi": addi,
    "muli": muli,
    "bani": bani,
    "bori": bori,
    "seti": seti,
    "gtri": gtri,
    "eqri": eqri,
    "gtir": gtir,
    "eqir": eqir,
}


def run_vm(instructions, ip_reg):
    registers = [0, 0, 0, 0, 0, 0]

    ip = registers[ip_reg]
    while 0 <= ip < len(instructions):
        op_code, a, b, c = instructions[ip].split()
        a, b, c = int(a), int(b), int(c)

        op_func = ops_dict[op_code]
        registers = op_func(registers, a, b, c)
        registers[ip_reg] += 1
        ip = registers[ip_reg]

        if registers[ip_reg] == 28:
            break

    return registers[3]


def part2():
    seen = set()
    prev = None
    a = 0
    while True:
        a |= 0x10000
        b = 15028787
        b += a & 0xff
        b &= 0xffffff
        b *= 65899
        b &= 0xffffff
        b += (a >> 8) & 0xff
        b &= 0xffffff
        b *= 65899
        b &= 0xffffff
        b += (a >> 16) & 0xff
        b &= 0xffffff
        b *= 65899
        b &= 0xffffff

        if b in seen:
            return prev
        else:
            seen.add(b)
            prev = b
            a = b


if __name__ == "__main__":
    with open("21.txt") as f:
        data = f.read().strip().split("\n")

    ip_reg = int(data[0].split()[-1])
    instructions = data[1:]

    part1 = run_vm(instructions, ip_reg)
    print("Part 1: {}".format(part1))

    print("Part 2: {}".format(part2()))
