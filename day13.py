def fold_along_y(coords, y_coord):
    # dots will never appear on a fold line
    return {(x, y if y < y_coord else y_coord - (y - y_coord)) for x, y in coords}


def fold_along_x(coords, x_coord):
    # dots will never appear on a fold line
    return {(x if x < x_coord else x_coord - (x - x_coord), y) for x, y in coords}


def fold(coords, instr):
    coord, amount = instr
    if coord == 'x':
        return fold_along_x(coords, amount)
    elif coord == 'y':
        return fold_along_y(coords, amount)
    else:
        raise ValueError(f'Invalid coord {coord}')


def fold_all(coords, folds):
    for instr in folds:
        coords = fold(coords, instr)
    return coords


def print_coords(coords):
    max_x = max((x for x, y in coords))
    max_y = max((y for x, y in coords))
    for y in range(max_y + 1):
        print(''.join('#' if (x, y) in coords else ' ' for x in range(max_x + 1)))


def get_solution():
    with open('input/day13_input.txt') as f:
        raw = ''.join(f.readlines())
    raw1 = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''
    coords_raw, folding_raw = tuple(raw.split('\n\n'))
    coords = {tuple(map(int, coord.strip().split(','))) for coord in coords_raw.split('\n')}
    folds = [(line[11], int(line.strip()[13:])) for line in folding_raw.split('\n') if line.strip()]
    print(len(fold(coords, folds[0])))
    result = fold_all(coords, folds)
    print_coords(result)
