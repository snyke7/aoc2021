def octopus_step(octopi):
    initial = [[(o + 1) % 10 for o in oline] for oline in octopi]
    flashed = [(i, j) for i in range(len(octopi)) for j in range(len(octopi[i])) if initial[i][j] == 0]
    while flashed:
        i, j = flashed.pop()
        prev_len = len(flashed)
        new_flashes = []
        if i > 0 and initial[i - 1][j] != 0:
            initial[i - 1][j] += 1
            initial[i - 1][j] %= 10
            if initial[i - 1][j] == 0:
                new_flashes.append((i - 1, j))
        if i < len(octopi) - 1 and initial[i + 1][j] != 0:
            initial[i + 1][j] += 1
            initial[i + 1][j] %= 10
            if initial[i + 1][j] == 0:
                new_flashes.append((i + 1, j))
        if j > 0 and initial[i][j - 1] != 0:
            initial[i][j - 1] += 1
            initial[i][j - 1] %= 10
            if initial[i][j - 1] == 0:
                new_flashes.append((i, j - 1))
        if j < len(octopi) - 1 and initial[i][j + 1] != 0:
            initial[i][j + 1] += 1
            initial[i][j + 1] %= 10
            if initial[i][j + 1] == 0:
                new_flashes.append((i, j + 1))
        if i > 0 and j > 0 and initial[i - 1][j - 1] != 0:
            initial[i - 1][j - 1] += 1
            initial[i - 1][j - 1] %= 10
            if initial[i - 1][j - 1] == 0:
                new_flashes.append((i - 1, j - 1))
        if i < len(octopi) - 1 and j > 0 and initial[i + 1][j - 1] != 0:
            initial[i + 1][j - 1] += 1
            initial[i + 1][j - 1] %= 10
            if initial[i + 1][j - 1] == 0:
                new_flashes.append((i + 1, j - 1))
        if i > 0 and j < len(octopi) - 1 and initial[i - 1][j + 1] != 0:
            initial[i - 1][j + 1] += 1
            initial[i - 1][j + 1] %= 10
            if initial[i - 1][j + 1] == 0:
                new_flashes.append((i - 1, j + 1))
        if i < len(octopi) - 1 and j < len(octopi) - 1 and initial[i + 1][j + 1] != 0:
            initial[i + 1][j + 1] += 1
            initial[i + 1][j + 1] %= 10
            if initial[i + 1][j + 1] == 0:
                new_flashes.append((i + 1, j + 1))
        flashed.extend(new_flashes)
    return initial


def count_flashes(octopus):
    return sum((1 for oline in octopus for o in oline if o == 0))


def octopus_steps(octopus, steps):
    result = octopus
    flashes = 0
    for i in range(steps):
        result = octopus_step(result)
        flashes += count_flashes(result)
    return result, flashes


def find_all_flashing(octopus):
    steps = 0
    while count_flashes(octopus) != len(octopus) ** 2:
        octopus = octopus_step(octopus)
        steps += 1
    return steps


def print_octo(octopus):
    print('\n'.join((''.join(str(o) for o in oline)) for oline in octopus))


def get_solution():
    with open('input/day11_input.txt') as f:
        lines = f.readlines()
#     lines = '''5483143223
# 2745854711
# 5264556173
# 6141336146
# 6357385478
# 4167524645
# 2176841721
# 6882881134
# 4846848554
# 5283751526'''.splitlines()
    octopi = [[int(c) for c in line.strip()] for line in lines]
    result, flashes = octopus_steps(octopi, 100)
    print(flashes)
    print(find_all_flashing(octopi))

