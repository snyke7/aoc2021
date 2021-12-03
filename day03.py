test = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
'''


def get_solution_from_lines(lines):
    numbers = [line.strip() for line in lines]
    cols = len(numbers[0])
    num_nums = len(numbers)
    gamma = int(''.join((('1' if sum((int(num[col]) for num in numbers)) > num_nums / 2 else '0') for col in range(cols))), 2)
    eps = 2 ** cols - gamma - 1
    return gamma, eps


def get_solution2_from_lines(lines, swap=False):
    numbers = [line.strip() for line in lines]
    cols = len(numbers[0])
    col = 0
    while True:
        to_keep = '1' if swap ^ (sum((int(num[col]) for num in numbers)) >= len(numbers) / 2) else '0'
        numbers = [num for num in numbers if num[col] == to_keep]
        if len(numbers) == 1:
            return int(numbers[0], 2)
        col += 1
        if col >= cols:
            raise ValueError()


def get_solution():
    with open('input/day03_input.txt') as f:
        lines = f.readlines()
    gamma, eps = get_solution_from_lines(lines)
    print(gamma * eps)
    # gamma, eps = get_solution_from_lines(test.splitlines())
    # print(gamma * eps)
    oxygen = get_solution2_from_lines(lines)
    co2 = get_solution2_from_lines(lines, True)
    print(oxygen * co2)
