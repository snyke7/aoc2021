def get_score(crabs, pos):
    return sum((abs(crab - pos) for crab in crabs))


def get_score_pt2(crabs, pos):
    return sum(((abs(crab - pos)) * (abs(crab - pos) + 1)) // 2 for crab in crabs)


def get_best_pos(crabs, score_fun=get_score):
    best_score = float('infinity')
    best_pos = None
    for p in range(min(crabs), max(crabs)):
        score = score_fun(crabs, p)
        if score < best_score:
            best_score = score
            best_pos = p
    return best_pos, best_score


def get_solution():
    with open('input/day07_input.txt') as f:
        crabs = [int(crab) for crab in f.readlines()[0].strip().split(',')]
    print(get_best_pos(crabs))
    print(get_best_pos(crabs, get_score_pt2))
