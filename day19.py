from collections import defaultdict


def parse_scanner(scanner_str):
    coords_str = scanner_str.strip().split('\n')[1:]  # first line is '--- scanner x ---'
    return [tuple(map(int, line.strip().split(','))) for line in coords_str]


def get_abs_diffs(b1, b2):
    return [abs(b1c - b2c) for b1c, b2c in zip(b1, b2)]


def get_abs_diff_sum(b1, b2):
    return sum(get_abs_diffs(b1, b2))


def get_abs_diff_sum_map(beacons):
    diff_map = defaultdict(lambda: list())
    for i in range(len(beacons)):
        for j in range(i + 1, len(beacons)):
            diff_map[get_abs_diff_sum(beacons[i], beacons[j])].append((i, j))
    return dict(diff_map)


def get_coord_diff_map(b1, b2):
    result = defaultdict(lambda: list())
    for i in range(3):
        result[abs(b1[i] - b2[i])].append((i, 1 if b1[i] - b2[i] > 0 else -1 if b1[i] - b2[i] < 0 else 0))
    return dict(result)


def get_coord_maps(d_mapl, d_mapr):
    for a_diff in d_mapl.keys():
        if len(d_mapl[a_diff]) != len(d_mapr[a_diff]):
            return []
    result_base = {
        c_sgn_pr[0][0]: (d_mapr[a_diff][0][0], 1 if d_mapr[a_diff][0][1] == c_sgn_pr[0][1] else -1)
        for a_diff, c_sgn_pr in d_mapl.items()
        if a_diff != 0 and len(c_sgn_pr) == 1
    }
    if len(result_base) == 3:
        # there is only one option
        return [result_base]
    # maybe we need to compute other options, but that seems difficult. try to get away with no options for now
    return []


def sub_beacon(b1, b2):
    return b1[0] - b2[0], b1[1] - b2[1], b1[2] - b2[2]


def add_beacon(b1, b2):
    return b1[0] + b2[0], b1[1] + b2[1], b1[2] + b2[2]


def compose_cmaps(cmapl, cmapr):
    return {
        0: (cmapr[cmapl[0][0]][0], cmapr[cmapl[0][0]][1] * cmapl[0][1]),
        1: (cmapr[cmapl[1][0]][0], cmapr[cmapl[1][0]][1] * cmapl[1][1]),
        2: (cmapr[cmapl[2][0]][0], cmapr[cmapl[2][0]][1] * cmapl[2][1]),
    }


def transform_beacon_coord(beacon, coord_map):
    return (
        beacon[coord_map[0][0]] * coord_map[0][1],
        beacon[coord_map[1][0]] * coord_map[1][1],
        beacon[coord_map[2][0]] * coord_map[2][1],
    )


def extend_to_shared(scan_l, scan_r, coord_map, li, ri):
    li_centered_beacons = [sub_beacon(scan_l[li], b1) for b1 in scan_l if b1 != scan_l[li]]
    ri_centered_beacons = [
        transform_beacon_coord(sub_beacon(scan_r[ri], b1), coord_map)
        for b1 in scan_r if b1 != scan_r[ri]
    ]
    if len(set(li_centered_beacons) & set(ri_centered_beacons)) >= 11:
        # we have a match, now calculate relative position of scan_r to scan_l
        return sub_beacon(scan_l[li], transform_beacon_coord(scan_r[ri], coord_map)), coord_map
    else:
        return False


def try_extend_to_shared_beacons(l_idxs, r_idxs, scan_l, scan_r):
    li, lj = l_idxs
    ri, rj = r_idxs
    abs_dl = get_abs_diffs(scan_l[li], scan_l[lj])
    abs_dr = get_abs_diffs(scan_r[ri], scan_r[rj])
    if len(set(abs_dl)) != len(set(abs_dr)):
        return None
    if len(set(abs_dl) & set(abs_dr)) < len(set(abs_dl)):
        return None
    d_mapl = get_coord_diff_map(scan_l[li], scan_l[lj])
    d_mapr = get_coord_diff_map(scan_r[ri], scan_r[rj])
    for coord_map in get_coord_maps(d_mapl, d_mapr):
        result = extend_to_shared(scan_l, scan_r, coord_map, li, ri)
        if result:
            return result
    return None


def detect_relative_position(scan_l, scan_r):
    diffs_l = get_abs_diff_sum_map(scan_l)
    diffs_r = get_abs_diff_sum_map(scan_r)
    shared_diffs = set(diffs_l.keys()) & set(diffs_r.keys())
    for diff in shared_diffs:
        for l_idxs in diffs_l[diff]:  # this will usually have low multiplicity
            for r_idxs in diffs_r[diff]:  # as will this
                result = try_extend_to_shared_beacons(l_idxs, r_idxs, scan_l, scan_r)
                if result:
                    return result


def detect_any_relative_scanner(scanner, rem_scanners):
    for i, scanner2 in rem_scanners.items():
        result = detect_relative_position(scanner, scanner2)
        if result:
            return i, result[0], result[1]
    return None


def find_all_relative_positions(scanners):
    result = {0: ((0, 0, 0), {0: (0, 1), 1: (1, 1), 2: (2, 1)})}
    new_scanners = {0}
    rem_scanners = dict(enumerate(scanners))
    del rem_scanners[0]
    while new_scanners:
        idx = new_scanners.pop()
        scanner = scanners[idx]
        try_detect = True
        while try_detect:
            res = detect_any_relative_scanner(scanner, rem_scanners)
            try_detect = res is not None
            if res:
                i, rel_pos, c_map = res  # rel_pos to idx, not to zero
                del rem_scanners[i]
                new_scanners.add(i)
                result[i] = add_beacon(transform_beacon_coord(rel_pos, result[idx][1]), result[idx][0]), compose_cmaps(result[idx][1], c_map)
    return result


def get_beacons(scanners, rel_positions):
    beacon_set = {
        add_beacon(transform_beacon_coord(beacon, rel_positions[i][1]), rel_positions[i][0])
        for i, scanner in enumerate(scanners)
        for beacon in scanner
    }
    return beacon_set


def get_largest_dist(rel_positions):
    only_rel_positions = [val[0] for val in rel_positions.values()]
    max_dist = 0
    for rel_pos1 in only_rel_positions:
        for rel_pos2 in only_rel_positions:
            manhattan_dist = get_abs_diff_sum(rel_pos1, rel_pos2)
            if manhattan_dist > max_dist:
                max_dist = manhattan_dist
    return max_dist


def get_solution():
    with open('input/day19_input.txt') as f:
        lines = ''.join(f.readlines())
    scanners = [parse_scanner(scanner_raw) for scanner_raw in lines.split('\n\n')]
    shared_beacons = detect_relative_position(scanners[0], scanners[1])
    # test = dict(enumerate(scanners))
    # del test[0]
    # print(detect_any_relative_scanner(scanners[0], test))
    result = find_all_relative_positions(scanners)
    all_beacons = get_beacons(scanners, result)
    print(len(all_beacons))
    print(get_largest_dist(result))
    # scanner zero:
    # -618, -824, -621
    # -537, -823, -458  -> abs diff 81, 1, 163 sum = 245
    # scanner one:
    # 686,422,578
    # 605,423,415
    # rel pos: 68,-1246,-43  -618 - 686
    # scanner 3 must be at -92,-2380,-20
    # is relative to 1 at (160, -1134, -23)
    # 1 is relative to 0 at (68, -1246, -43)
