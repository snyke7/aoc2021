def to_enh_alg(line):
    return dict(enumerate([1 if c == '#' else 0 for c in line]))


def parse_pic(pic_str):
    return [
        [1 if c == '#' else 0 for c in line.strip()]
        for line in pic_str.splitlines()
    ], 0


def get_val_at(raw_pic, outside_val, i, j):
    if 0 <= i < len(raw_pic):
        if 0 <= j < len(raw_pic[i]):
            return raw_pic[i][j]
    return outside_val


def compute_enh_at(input_pic, i, j, enh_alg, outside_val):
    def get_my_val(n, m):
        return get_val_at(input_pic, outside_val, n, m)
    the_vals = [
        get_my_val(i - 1, j - 1),
        get_my_val(i - 1, j),
        get_my_val(i - 1, j + 1),
        get_my_val(i, j - 1),
        get_my_val(i, j),
        get_my_val(i, j + 1),
        get_my_val(i + 1, j - 1),
        get_my_val(i + 1, j),
        get_my_val(i + 1, j + 1),
    ]
    bin_val = sum((2 ** i * val for i, val in enumerate(reversed(the_vals))))
    return enh_alg[bin_val]


def enhance_pic(input_pic, enh_alg):
    pic, outside_val = input_pic
    bigger_pic = [
        [compute_enh_at(pic, i, j, enh_alg, outside_val) for j in range(-1, len(pic) + 1)]
        for i in range(-1, len(pic) + 1)
    ]
    new_outside_val = enh_alg[int(9*str(outside_val), 2)]
    return bigger_pic, new_outside_val


def print_pic(the_pic):
    raw_pic, _ = the_pic
    for line in raw_pic:
        print(''.join(['#' if v else '.' for v in line]))
    print()


def enhance_pic_times(pic, alg, times):
    for _ in range(times):
        pic = enhance_pic(pic, alg)
    return pic


def count_pixels(pic):
    raw_pic, outside_val = pic
    if outside_val == 1:
        return float('inf')
    return sum(map(sum, raw_pic))


def get_solution():
    with open('input/day20_input.txt') as f:
        lines = f.readlines()
    enh_alg = to_enh_alg(lines[0].strip())
    input_pic = parse_pic(''.join(lines[2:]))
    enhanced = enhance_pic_times(input_pic, enh_alg, 2)
    print(count_pixels(enhanced))
    enhanced_alot = enhance_pic_times(input_pic, enh_alg, 50)
    print(count_pixels(enhanced_alot))
