from parsy import string, decimal_digit, generate, alt

snail_raw_num = decimal_digit.at_least(1).concat().map(int)


@generate
def snail_pair_num():
    yield string('[')
    left = yield alt(snail_raw_num, snail_pair_num)
    yield string(',')
    right = yield alt(snail_raw_num, snail_pair_num)
    yield string(']')
    return left, right


snail_num = snail_raw_num | snail_pair_num


def find_loc(num, the_lam, depth=0):
    if the_lam(num, depth):
        return tuple()
    if not isinstance(num, tuple):
        return None
    left, right = num
    left_expl = find_loc(left, the_lam, depth+1)
    if left_expl is not None:
        return (0,) + left_expl
    right_expl = find_loc(right, the_lam,depth+1)
    if right_expl is not None:
        return (1,) + right_expl
    return None


def get_explosion_loc(num):
    def is_expl_loc(the_num, depth):
        if not isinstance(the_num, tuple):
            return False
        return depth >= 4
    return find_loc(num, is_expl_loc)


def get_split_loc(num):
    def is_split_loc(the_num, depth):
        if isinstance(the_num, tuple):
            return False
        return the_num >= 10
    return find_loc(num, is_split_loc)


def get_num_at(num, loc):
    if not loc:
        return num
    if isinstance(num, tuple):
        left, right = num
        return get_num_at(left if loc[0] == 0 else right, loc[1:])
    else:
        raise ValueError(f'Non empty loc {loc} on num {num}')


def get_left_of(num, loc):
    trunc_loc = tuple(loc)
    while trunc_loc and trunc_loc[-1] == 0:
        trunc_loc = trunc_loc[:-1]
    if not trunc_loc:
        return None
    left_loc = trunc_loc[:-1] + (0,)
    while isinstance(get_num_at(num, left_loc), tuple):
        left_loc += (1,)
    return left_loc


def get_right_of(num, loc):
    trunc_loc = tuple(loc)
    while trunc_loc and trunc_loc[-1] == 1:
        trunc_loc = trunc_loc[:-1]
    if not trunc_loc:
        return None
    right_loc = trunc_loc[:-1] + (1,)
    while isinstance(get_num_at(num, right_loc), tuple):
        right_loc += (0,)
    return right_loc


def replace(orig, loc, new_val):
    if not loc:
        return new_val
    left, right = orig
    if loc[0] == 0:
        return replace(left, loc[1:], new_val), right
    elif loc[0] == 1:
        return left, replace(right, loc[1:], new_val)


def explode(num, expl_loc):
    left_val, right_val = get_num_at(num, expl_loc)
    # now find loc to the left and to the right of loc
    left_loc = get_left_of(num, expl_loc)
    right_loc = get_right_of(num, expl_loc)
    left_rep = replace(num, left_loc, get_num_at(num, left_loc) + left_val) if left_loc else num
    right_rep = replace(left_rep, right_loc, get_num_at(num, right_loc) + right_val) if right_loc else left_rep
    rep_expl = replace(right_rep, expl_loc, 0)
    return rep_expl


def split(num, split_loc):
    val = get_num_at(num, split_loc)
    return replace(num, split_loc, (val // 2, val - val // 2))


def reduce(num):
    loc = get_explosion_loc(num)
    if loc:
        return reduce(explode(num, loc))
    loc = get_split_loc(num)
    if loc:
        return reduce(split(num, loc))
    return num


def add(num1, num2):
    return reduce((num1, num2))


def sum_snail_nums(nums):
    total = None
    for num in nums:
        if total is not None:
            total = add(total, num)
        else:
            total = num
    return total


def magnitude(num):
    if not isinstance(num, tuple):
        return num
    left, right = num
    return 3 * magnitude(left) + 2 * magnitude(right)


def get_largest_2sum(nums):
    largest = 0
    for num1 in nums:
        for num2 in nums:
            mag = max(magnitude(add(num1, num2)), magnitude(add(num2, num1)))
            if mag > largest:
                largest = mag
    return largest


def get_solution():
    with open('input/day18_input.txt') as f:
        lines = f.readlines()
    lines2 = '[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n[6,6]'.splitlines()
    snail_nums = [snail_num.parse(line.strip()) for line in lines]
    print(magnitude(sum_snail_nums(snail_nums)))
    print(get_largest_2sum(snail_nums))
