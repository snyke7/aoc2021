def to_bingo(bingo_str):
    return [
        [
            (int(num), False) for num in line.split()
        ] for line in bingo_str.strip().split('\n')
    ]


def update_bingo(num, bingo):
    for i in range(len(bingo)):
        for j in range(len(bingo[i])):
            num_at, marked = bingo[i][j]
            if marked:
                continue
            if num_at == num:
                bingo[i][j] = num_at, True
                return


def has_won(bingo):
    row_won = any((all((marked for num, marked in row)) for row in bingo))
    if row_won:
        return True
    col_won = any((all((bingo[j][i][1] for j in range(len(bingo)))) for i in range(len(bingo))))
    return col_won


def get_first_winners(nums, bingos):
    for num in nums:
        result = []
        for bingo in bingos:
            update_bingo(num, bingo)
            if has_won(bingo):
                result.append(bingo)
        if result:
            return result, num
    raise ValueError('no winner? :(')


def get_last_winner(nums, bingos):
    while len(bingos) > 1:
        winners, num = get_first_winners(nums, bingos)
        nums = nums[nums.index(num) + 1:]
        for winner in winners:
            bingos.remove(winner)
    last, num = get_first_winners(nums, bingos)
    return last[0], num


def get_score(bingo, winning_num):
    unmarked = sum((num for row in bingo for num, marked in row if not marked))
    return unmarked * winning_num


def print_bingo_win(bingo):
    print('_____')
    for row in bingo:
        print(''.join(('*' if marked else ' ' for num, marked in row)))
    print('_____')


def get_solution():
    with open('input/day04_input.txt') as f:
        lines = f.readlines()
    nums = [int(num) for num in lines[0].strip().split(',')]
    bingos = [to_bingo(line) for line in ''.join(lines[1:]).split('\n\n')]
    winners, num = get_first_winners(nums, bingos)
    winner = winners[0]
    last_winner, last_num = get_last_winner(nums, bingos)
    print(get_score(winner, num))
    print(get_score(last_winner, last_num))
