def update_shortest_path(coord, path_map, path_len):
    if (coord not in path_map) or path_map[coord] > path_len:
        path_map[coord] = path_len
        return True
    else:
        return False


def dijkstra(node_square):
    shortest_path_map = {(0, 0): 0}
    new_coords = {(0, 0)}
    max_dist = 0
    while new_coords:
        i, j = new_coords.pop()
        cur_len = shortest_path_map[(i, j)]
        updated = []
        if i > 0 and update_shortest_path((i - 1, j), shortest_path_map, cur_len + node_square[i - 1][j]):
            updated.append((i - 1, j))
        if i < len(node_square) - 1 and update_shortest_path((i + 1, j), shortest_path_map, cur_len + node_square[i + 1][j]):
            updated.append((i + 1, j))
        if j > 0 and update_shortest_path((i, j - 1), shortest_path_map, cur_len + node_square[i][j - 1]):
            updated.append((i, j - 1))
        if j < len(node_square[i]) - 1 and update_shortest_path((i, j + 1), shortest_path_map, cur_len + node_square[i][j + 1]):
            updated.append((i, j + 1))
        new_coords.update(updated)
    return shortest_path_map[(len(node_square) - 1, len(node_square) - 1)]


def extend_node_square(node_square):
    return [[(c + i + j - 1) % 9 + 1 for j in range(5) for c in line]for i in range(5) for line in node_square]


def get_solution():
    with open('input/day15_input.txt') as f:
        lines = f.readlines()
    lines1 = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''.splitlines()
    node_square = [[int(c) for c in line.strip()] for line in lines]
    print(dijkstra(node_square))
    print(dijkstra(extend_node_square(node_square)))

