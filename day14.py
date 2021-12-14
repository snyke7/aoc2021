from collections import defaultdict


def polymer_step(polymer, rules):
    to_zip_with = [rules[prv + nxt] if (prv + nxt) in rules else '' for prv, nxt in zip(polymer[:-1], polymer[1:])]
    return ''.join((orig + zippart for orig, zippart in zip(polymer, to_zip_with + [''])))


def polymer_steps(polymer, rules, steps):
    for i in range(steps):
        polymer = polymer_step(polymer, rules)
    return polymer


def calc_score(polymer):
    comps = set(polymer)
    occ_map = {comp: len([1 for c in polymer if c == comp]) for comp in comps}
    return max(occ_map.values()) - min(occ_map.values())


def as_pair_dict(polymer):
    pair_list = [prv + nxt for prv, nxt in zip(polymer[:-1], polymer[1:])]
    return {pair: len([1 for pr in pair_list if pr == pair]) for pair in set(pair_list)}


def polymer_step_pairdict(pairdict, rules):
    result = defaultdict(lambda: 0)
    for pair, amt in pairdict.items():
        between = rules[pair]
        result[pair[0] + between] += amt
        result[between + pair[1]] += amt
    return dict(result)


def polymer_steps_pairdict(pairdict, rules, steps):
    for i in range(steps):
        pairdict = polymer_step_pairdict(pairdict, rules)
    return pairdict


def calc_score_pairdict(pairdict, initial):
    occ_map = defaultdict(lambda: 0)
    for pair, amt in pairdict.items():
        occ_map[pair[0]] += amt
    occ_map[initial[-1]] += 1
    return max(occ_map.values()) - min(occ_map.values())


def get_solution():
    with open('input/day14_input.txt') as f:
        lines = f.readlines()
    lines1 = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''.splitlines()
    base = lines[0].strip()
    rules = dict([tuple(line.strip().split(' -> ')) for line in lines[2:]])
    final = polymer_steps(base, rules, 10)
    print(calc_score(final))
    pairs_base = as_pair_dict(base)
    final2 = polymer_steps_pairdict(pairs_base, rules, 40)
    print(calc_score_pairdict(final2, base))
