def get_solution():
    with open('input/day01_input.txt') as f:
        numbers = [int(line.strip()) for line in f.readlines()]
    diffs = [num2 - num1 for num1, num2 in zip(numbers[:-1], numbers[1:])]
    print(len([diff for diff in diffs if diff > 0]))
    sum3s = [num1 + num2 + num3 for num1, num2, num3 in zip(numbers, numbers[1:], numbers[2:])]
    diff3s = [num2 - num1 for num1, num2 in zip(sum3s[:-1], sum3s[1:])]
    print(len([diff for diff in diff3s if diff > 0]))
