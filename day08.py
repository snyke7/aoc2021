REAL_SEGMENTS = {
    1: set('cf'),
    7: set('acf'),
    4: set('bcdf'),
    2: set('acdeg'),
    3: set('acdfg'),
    5: set('abdfg'),
    0: set('abcefg'),
    6: set('abdefg'),
    9: set('abcdfg'),
    8: set('abcdefg'),
}


def determine_wiring(digits):
    one_digits = next((digit for digit in digits if len(digit) == 2))
    seven_digits = next((digit for digit in digits if len(digit) == 3))
    four_digits = next((digit for digit in digits if len(digit) == 4))
    a_letter = next(iter(set(seven_digits) - set(one_digits)))
    bfg_letters = set.intersection(*(digit for digit in digits if len(digit) == 6)) - {a_letter}
    c_letter = (one_digits - bfg_letters).pop()
    f_letter = (one_digits - {c_letter}).pop()
    d_letter = (four_digits - bfg_letters - {c_letter}).pop()
    b_letter = (four_digits - {c_letter, d_letter, f_letter}).pop()
    nine_digits = next((digit for digit in digits
                        if {a_letter, b_letter, c_letter, d_letter, f_letter}.issubset(digit) and len(digit) == 6))
    g_letter = (nine_digits - {a_letter, b_letter, c_letter, d_letter, f_letter}).pop()
    eight_digits = next((digit for digit in digits if len(digit) == 7))
    e_letter = (eight_digits - {a_letter, b_letter, c_letter, d_letter, g_letter, f_letter}).pop()
    return {
        'a': a_letter,
        'b': b_letter,
        'c': c_letter,
        'd': d_letter,
        'e': e_letter,
        'f': f_letter,
        'g': g_letter,
    }


def determine_output(wiring, output_digits):
    reverse_wiring = {val: key for key, val in wiring.items()}
    original_segments = [{reverse_wiring[segment] for segment in digit} for digit in output_digits]
    original_numbers = [key for segments in original_segments for key, val in REAL_SEGMENTS.items() if segments == val]
    return int(''.join(map(str, original_numbers)))


def get_output(line):
    all_digits, output_digit = tuple(line.split('|'))
    wiring = determine_wiring([set(digit) for digit in all_digits.strip().split()])
    return determine_output(wiring, [set(digit) for digit in output_digit.split()])


def get_solution():
    test_input = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''
    test_one = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'
    with open('input/day08_input.txt') as f:
        the_lines = f.readlines()
    # the_lines = test_input.splitlines()
    output_digits = [line.split('|')[1].strip().split() for line in the_lines]
    print(sum((1 for output in output_digits for digit in output if len(digit) in {2, 3, 4, 7})))
    print(sum((get_output(line) for line in the_lines)))
