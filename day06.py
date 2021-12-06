def day_step(fish_dict):
    new_fish_dict = {i: fish_dict[i + 1] for i in range(0, 7+1)}
    new_fish_dict[6] += fish_dict[0]
    new_fish_dict[8] = fish_dict[0]
    return new_fish_dict


def day_steps(fish_dict, days):
    for i in range(days):
        fish_dict = day_step(fish_dict)
    return fish_dict


def get_solution():
    with open('input/day06_input.txt') as f:
        fishes = list(map(int, f.readlines()[0].strip().split(',')))
    # fishes = [3, 4, 3, 1, 2]
    fish_dict = {i: 0 for i in range(0, 8+1)}
    for fish in fishes:
        fish_dict[fish] += 1
    # print(fish_dict)
    print(sum(day_steps(fish_dict, 256).values()))

