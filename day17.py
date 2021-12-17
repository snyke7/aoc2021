import math


def gety(v_y, t):
    return t * v_y - (t * (t - 1)) // 2


def getx(v_x, t):
    # assumes v_x and v_y > 0
    if t > v_x:
        return getx(v_x, v_x)
    return gety(v_x, t)


def get_pos(v_x, v_y, t):
    # assumes v_x and v_y > 0
    return getx(v_x, t), gety(v_y, t)


def get_min_vx(x_min):
    return math.ceil((-1.0 + math.sqrt(1.0 + 8.0 * x_min)) / 2.0)


def get_time_at(v, dest):
    if 2 * dest > v ** 2 + v:  # then does not reach
        return None
    return (1.0 + 2.0 * v - math.sqrt(4.0 * v ** 2 + 4.0 * v + 1.0 - 8.0 * dest)) / 2.0


def part_1(target_bounds):
    # assuming y_min < 0
    x_min, x_max, y_min, y_max = tuple(target_bounds)
    vx = get_min_vx(x_min)
    vy = -y_min - 1
    posx, posy = get_pos(vx, vy, 2 * vy + 2)
    assert(x_min <= posx <= x_max)
    assert(y_min <= posy <= y_max)
    return (vy ** 2 + vy) // 2


def is_in_bounds(pos, bounds):
    posx, posy = pos
    x_min, x_max, y_min, y_max = tuple(bounds)
    return x_min <= posx <= x_max and y_min <= posy <= y_max


def part_2(target_bounds):
    x_min, x_max, y_min, y_max = tuple(target_bounds)
    result = set()
    for vx in range(get_min_vx(x_min), x_max + 1):
        # now divine the times for which we are in the target area
        min_time = math.ceil(get_time_at(vx, x_min))
        max_time = get_time_at(vx, x_max)
        if max_time:  # then we only pass through the desired target area, x-wise
            max_time = math.ceil(max_time)
        else:  # at t >= v_x, the probe has zero x-velocity and is in the target area
            # this means the max_time necessary is - 2 * y_min
            max_time = -2 * y_min
        for t in range(min_time, max_time + 1):
            vy_min = math.ceil(y_min / t + (t - 1.0) / 2.0)
            vy_max = math.floor(y_max / t + (t - 1.0) / 2.0)
            result.update([(vx, vy) for vy in range(vy_min, vy_max + 1) if is_in_bounds(get_pos(vx, vy, t), target_bounds)])
    return result


def get_solution():
    target_bounds = [70, 96, -179, -124]
    target_bounds1 = [20, 30, -10, -5]
    print(part_1(target_bounds))
    result = part_2(target_bounds)
    print(len(result))
