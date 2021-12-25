from typing import List
from copy import deepcopy


def parse_line(line):
    return [
        0 if c == '.' else
        1 if c == '>' else
        2 if c == 'v' else
        1/0
        for c in line
    ]


def get_right_movables(cucumbers):
    return [
        (i, j)
        for i in range(len(cucumbers))
        for j in range(len(cucumbers[i]))
        if cucumbers[i][j] == 1 and cucumbers[i][(j + 1) % len(cucumbers[i])] == 0
    ]


def get_down_movables(cucumbers):
    return [
        (i, j)
        for i in range(len(cucumbers))
        for j in range(len(cucumbers[i]))
        if cucumbers[i][j] == 2 and cucumbers[(i + 1) % len(cucumbers)][j] == 0
    ]


def do_right_move(cucumbers: List[List[int]], right_move_locs):
    new_cucumbers = deepcopy(cucumbers)
    for i, j in right_move_locs:
        new_cucumbers[i][j] = 0
        new_cucumbers[i][(j + 1) % len(new_cucumbers[i])] = cucumbers[i][j]
    return new_cucumbers


def do_down_move(cucumbers: List[List[int]], down_move_locs):
    new_cucumbers = deepcopy(cucumbers)
    for i, j in down_move_locs:
        new_cucumbers[i][j] = 0
        new_cucumbers[(i + 1) % len(new_cucumbers)][j] = cucumbers[i][j]
    return new_cucumbers


def cucumber_step(cucumbers):
    right_moves = get_right_movables(cucumbers)
    cucumbers_right = do_right_move(cucumbers, right_moves)
    down_moves = get_down_movables(cucumbers_right)
    return do_down_move(cucumbers_right, down_moves), right_moves or down_moves


def cucumber_stuck(cucumbers):
    steps = 0
    progress = True
    while progress:
        cucumbers, progress = cucumber_step(cucumbers)
        steps += 1
    return cucumbers, steps


def get_solution():
    with open('input/day25_input.txt') as f:
        lines = f.readlines()
    lines2 = '''v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>'''.splitlines()
    cucumbers = [parse_line(line.strip()) for line in lines]
    print(cucumber_stuck(cucumbers)[1])
