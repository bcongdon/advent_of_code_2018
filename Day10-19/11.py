import numpy as np
SEED = 1308
n = 300


def calculate_power_level(x, y, seed):
    rack_id = x + 10
    power_level = ((rack_id * y) + seed) * rack_id
    power_level = (power_level // 100) % 10
    return power_level - 5


def make_grid():
    grid = np.zeros((n, n))

    for x in range(n):
        for y in range(n):
            grid[x,y] = calculate_power_level(x+1, y+1, SEED)
    return grid

def part1():
    grid = make_grid()
    m_x, m_y, m_sum = 0, 0, 0
    for x in range(n - 3):
        for y in range(n - 3):
            total = np.sum(grid[x:x+3, y:y+3])
            if total > m_sum:
                m_sum = total
                m_x, m_y = x, y
    return m_x+1, m_y+1


def part2():
    grid = make_grid()
    m_x, m_y, m_sum, m_width = 0, 0, 0, 0
    for w in range(1, 300):
        print(w, m_x+1, m_y+1, m_width, m_sum)
        for x in range(n-3):
            for y in range(n-3):
                total = np.sum(grid[x:x+w, y:y+w])
                if total > m_sum:
                    m_x, m_y = x, y
                    m_sum, m_width = total, w
    return m_x+1, m_y+1, m_width

if __name__ == '__main__':
    print("Part 1: {}".format(part1()))
    print("Part 2: {}".format(part2()))
