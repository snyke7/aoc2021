def is_low_point(depths, i, j):
    depth = depths[i][j]
    if i > 0 and depths[i - 1][j] <= depth:
        return False
    if i < len(depths) - 1 and depths[i + 1][j] <= depth:
        return False
    if j > 0 and depths[i][j - 1] <= depth:
        return False
    if j < len(depths[i]) - 1 and depths[i][j + 1] <= depth:
        return False
    return True


def get_low_points(depths):
    return [
        (depth, i, j)
        for i, depthline in enumerate(depths)
        for j, depth in enumerate(depthline)
        if is_low_point(depths, i, j)
    ]


def get_basin(starti, startj, depths):
    new_points = [(starti, startj)]
    basin = {(starti, startj)}
    while new_points:
        i, j = new_points.pop()
        depth = depths[i][j]
        flow_neighbors = []
        if i > 0 and depths[i - 1][j] > depth and depths[i - 1][j] != 9:
            flow_neighbors.append((i - 1, j))
        if i < len(depths) - 1 and depths[i + 1][j] > depth and depths[i + 1][j] != 9:
            flow_neighbors.append((i + 1, j))
        if j > 0 and depths[i][j - 1] > depth and depths[i][j - 1] != 9:
            flow_neighbors.append((i, j - 1))
        if j < len(depths[i]) - 1 and depths[i][j + 1] > depth and depths[i][j + 1] != 9:
            flow_neighbors.append((i, j + 1))
        for neighb in flow_neighbors:
            if neighb not in basin:
                basin.add(neighb)
                new_points.append(neighb)
    return basin


def get_solution():
    with open('input/day09_input.txt') as f:
        the_lines = f.readlines()
#     the_lines = '''2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678'''.splitlines()
    depths = [[int(char) for char in line.strip()] for line in the_lines]
    low_points = get_low_points(depths)
    risk_sum = sum((depth for depth, _, _ in low_points)) + len(low_points)
    print(risk_sum)
    basin_sizes = list(reversed(sorted([len(get_basin(pti, ptj, depths)) for _, pti, ptj in low_points])))
    print(basin_sizes[0] * basin_sizes[1] * basin_sizes[2])

