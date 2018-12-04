import numpy as np

def parse_line(line):
    pieces = line.split(' ')
    c_id = pieces[0][1:]
    x, y = pieces[2].split(',')
    dx, dy = pieces[-1].split('x')
    return c_id, int(x), int(y[:-1]), int(dx), int(dy)

def part1(claims):
    max_x = max(c[1] + c[3] for c in claims)
    max_y = max(c[2] + c[4] for c in claims)
    arr = np.zeros((max_x, max_y))

    for c in claims:
        _, x, y, dx, dy = c
        arr[x:x+dx,y:y+dy] += 1
    
    return np.sum(arr > 1)

def part2(claims):
    max_x = max(c[1] + c[3] for c in claims)
    max_y = max(c[2] + c[4] for c in claims)
    arr = np.zeros((max_x, max_y))

    for c in claims:
        _, x, y, dx, dy = c
        arr[x:x+dx,y:y+dy] += 1

    for c in claims:
        c_id, x, y, dx, dy = c
        if np.all(arr[x:x+dx, y:y+dy] == 1):
            return c_id
    
if __name__ == '__main__':
    with open('3.txt') as f:
        data = f.readlines()

    parsed = [parse_line(line) for line in data]
    print('Part 1: {}'.format(part1(parsed)))
    print('Part 2: {}'.format(part2(parsed)))
