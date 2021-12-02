def as_coord(line):
    direction, amount = tuple(line.split(' '))
    if direction == 'forward':
        return int(amount), 0
    elif direction == 'down':
        return 0, int(amount)
    elif direction == 'up':
        return 0, -int(amount)
    else:
        raise ValueError(f'Unknown direction {direction}')


def solution_part2(coords):
    aim = 0
    depth = 0
    hor_pos = 0
    for fwd, aim_change in coords:
        aim += aim_change
        hor_pos += fwd
        depth += aim * fwd
    return hor_pos * depth


def get_solution():
    with open('input/day02_input.txt') as f:
        coords = [as_coord(line.strip()) for line in f.readlines()]
    hor_pos = sum((pos1 for pos1, pos2 in coords))
    vert_pos = sum((pos2 for pos1, pos2 in coords))
    print(hor_pos * vert_pos)
    print(solution_part2(coords))
