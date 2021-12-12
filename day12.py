from collections import defaultdict


def as_cave_dict(lines):
    result = defaultdict(lambda: set())
    for line in lines:
        left, right = tuple(line.strip().split('-'))
        result[left].add(right)
        result[right].add(left)
    return dict(result)


def is_valid_path_extension(path, app):
    if app.isupper():
        return True
    else:
        return app not in path


def is_valid_path_extension_pt2(path, app):
    if app.isupper():
        return True
    else:
        if app not in path:
            return True
        if app in {'start', 'end'}:  # start and end may never be visited twice
            return False
        # only a single small cave may be visited twice. only allow app if no small cave has been visited twice yet
        small_caves = [cave for cave in path if cave.islower()]
        return len(set(small_caves)) == len(small_caves)


def get_valid_paths(cave_dict, start, end, valid_path_checker=is_valid_path_extension):
    path_queue = [[start]]
    result = []
    while path_queue:
        cur_path = path_queue.pop()
        for ext in cave_dict[cur_path[-1]]:
            if not valid_path_checker(cur_path, ext):
                continue
            path_queue.append(cur_path + [ext])
            if ext == end:
                result.append(cur_path + [ext])
    return result


def get_solution():
    with open('input/day12_input.txt') as f:
        lines = f.readlines()
    lines1 = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''.splitlines()
    lines2 = '''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc'''.splitlines()
    lines3 = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''.splitlines()
    cave_dict = as_cave_dict(lines)
    print(len(get_valid_paths(cave_dict, 'start', 'end')))
    print(len(get_valid_paths(cave_dict, 'start', 'end', is_valid_path_extension_pt2)))
