class NavSyntaxError(ValueError):
    def __init__(self, illegal_char, expected):
        self.illegal_char = illegal_char
        self.expected = expected

    def __str__(self):
        return f'Syntax error: Expected {self.expected} but found {self.illegal_char} instead'


class NavIncompleteError(ValueError):
    def __init__(self, expected):
        self.expected = expected

    def __str__(self):
        return f'Incomplete syntax error: expected {self.expected} to close chunk'


OPEN_TO_CLOSE = {
    '[': ']',
    '(': ')',
    '{': '}',
    '<': '>'
}


def is_new_chunk(rem_line):
    return len(rem_line) > 0 and rem_line[0] in OPEN_TO_CLOSE.keys()


def parse_line(rem_line):
    if not rem_line:
        return None, ''
    if not is_new_chunk(rem_line):  # rem_line starts with closing character
        raise NavSyntaxError(rem_line[0], 'an opening character')
    closer = OPEN_TO_CLOSE[rem_line[0]]
    content = []
    content_line = rem_line[1:]
    while is_new_chunk(content_line):
        next_content, content_line = parse_line(content_line)
        content.append(next_content)
    # content_line is now either: empty or a closing character. empty means incomplete
    if not content_line:
        raise NavIncompleteError(closer)
    if content_line[0] == closer:
        return (rem_line[0], content), content_line[1:]
    else:  # wrong closing token
        raise NavSyntaxError(content_line[0], closer)


def parse_entire_line(line):
    rem_line = line
    result = []
    while rem_line:
        part, rem_line = parse_line(rem_line)
        result.append(part)
    return result


SYNTAX_ERROR_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


def get_error_score(lines):
    score = 0
    for line in lines:
        try:
            result = parse_entire_line(line)
        except NavIncompleteError:
            pass
        except NavSyntaxError as e:
            score += SYNTAX_ERROR_SCORE[e.illegal_char]
    return score


SYNTAX_AUTOCOMPLETE_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def is_incomplete(line):
    try:
        result = parse_entire_line(line)
        return False
    except NavSyntaxError:
        return False
    except NavIncompleteError:
        return True


def get_autocomplete_score(line):
    is_done = False
    line_score = 0
    while not is_done:
        try:
            result = parse_entire_line(line)
            is_done = True
        except NavIncompleteError as e:
            to_append = e.expected
            line_score *= 5
            line_score += SYNTAX_AUTOCOMPLETE_SCORE[to_append]
            line += to_append
    return line_score


def get_solution():
    with open('input/day10_input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
#     lines = '''[({(<(())[]>[[{[]{<()<>>
# [(()[<>])]({[<{<<[]>>(
# {([(<{}[<>[]}>{[]{[(<()>
# (((({<>}<{<{<>}{[]{[]{}
# [[<[([]))<([[{}[[()]]]
# [{[{({}]{}}([{[{{{}}([]
# {<[[]]>}<{[{[{[]{()[[[]
# [<(<(<(<{}))><([]([]()
# <{([([[(<>()){}]>(<<{{
# <{([{{}}[<[[[<>{}]]]>[]]'''.splitlines()
    print(get_error_score(lines))
    incomplete_scores = sorted([get_autocomplete_score(line) for line in lines if is_incomplete(line)])
    print(incomplete_scores[(len(incomplete_scores) + 1) // 2 - 1])
