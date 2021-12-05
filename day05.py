from collections import defaultdict


def to_coords(line):
    start, end = tuple(line.split(' -> '))
    return tuple(map(int, start.split(','))), tuple(map(int, end.split(',')))


def get_solution():
    with open('input/day05_input.txt') as f:
        coord_lines = [to_coords(line) for line in f.readlines()]
    num_vents = defaultdict(lambda: 0)
    for (startx, starty), (endx, endy) in coord_lines:
        if startx == endx:
            starty, endy = min(starty, endy), max(starty, endy)
            for y in range(starty, endy+1):
                num_vents[(startx, y)] += 1
        elif starty == endy:
            startx, endx = min(startx, endx), max(startx, endx)
            for x in range(startx, endx+1):
                num_vents[(x, starty)] += 1
        else:  # diagonal line
            dx = 1 if endx > startx else -1
            dy = 1 if endy > starty else -1
            curx = startx
            cury = starty
            for i in range(0, abs(startx - endx) + 1):
                num_vents[(curx, cury)] += 1
                curx += dx
                cury += dy
    avoid_points = {pt: vents for pt, vents in num_vents.items() if vents >= 2}
    print(avoid_points)
    print(len(avoid_points))

