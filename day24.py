from typing import List
import attr


# machine_state is a list of 4 + input word


class AbstractCmd:
    def run_command_on(self, machine_state) -> None:
        raise NotImplementedError


@attr.s(auto_attribs=True)
class InputCommand(AbstractCmd):
    index: int

    def run_command_on(self, machine_state) -> None:
        machine_state[self.index] = machine_state.pop(4)


class Operand:
    def get_value(self, machine_state) -> int:
        raise NotImplementedError


@attr.s(auto_attribs=True)
class ValueOperand(Operand):
    value: int

    def get_value(self, machine_state):
        return self.value


@attr.s(auto_attribs=True)
class PointerOperand(Operand):
    index: int

    def get_value(self, machine_state) -> int:
        return machine_state[self.index]


@attr.s(auto_attribs=True)
class AddCommand(AbstractCmd):
    index: int
    operand: Operand

    def run_command_on(self, machine_state) -> None:
        machine_state[self.index] += self.operand.get_value(machine_state)


@attr.s(auto_attribs=True)
class MulCommand(AbstractCmd):
    index: int
    operand: Operand

    def run_command_on(self, machine_state) -> None:
        machine_state[self.index] *= self.operand.get_value(machine_state)


@attr.s(auto_attribs=True)
class ModCommand(AbstractCmd):
    index: int
    operand: Operand

    def run_command_on(self, machine_state) -> None:
        machine_state[self.index] %= self.operand.get_value(machine_state)


@attr.s(auto_attribs=True)
class DivCommand(AbstractCmd):
    index: int
    operand: Operand

    def run_command_on(self, machine_state) -> None:
        machine_state[self.index] = machine_state[self.index] // self.operand.get_value(machine_state)


@attr.s(auto_attribs=True)
class EqCommand(AbstractCmd):
    index: int
    operand: Operand

    def run_command_on(self, machine_state) -> None:
        machine_state[self.index] = 1 if machine_state[self.index] == self.operand.get_value(machine_state) else 0


def get_index_for_operand(op_str):
    if op_str == 'w':
        return 0
    elif op_str == 'x':
        return 1
    elif op_str == 'y':
        return 2
    elif op_str == 'z':
        return 3


def parse_operand(op_str):
    try:
        return ValueOperand(int(op_str))
    except ValueError:
        return PointerOperand(get_index_for_operand(op_str))


def parse_line(line):
    cmd = line[:3]
    if cmd == 'inp':
        return InputCommand(get_index_for_operand(line[4]))
    op_l, op_r = tuple(line[4:].split())
    if cmd == 'add':
        return AddCommand(get_index_for_operand(op_l), parse_operand(op_r))
    elif cmd == 'mul':
        return MulCommand(get_index_for_operand(op_l), parse_operand(op_r))
    elif cmd == 'div':
        return DivCommand(get_index_for_operand(op_l), parse_operand(op_r))
    elif cmd == 'mod':
        return ModCommand(get_index_for_operand(op_l), parse_operand(op_r))
    elif cmd == 'eql':
        return EqCommand(get_index_for_operand(op_l), parse_operand(op_r))
    raise ValueError(f'Bad line: {line}')


def run_program(cmds: List[AbstractCmd], state):
    for cmd in cmds:
        cmd.run_command_on(state)
    return state


def initialize_state(input_list):
    return [0] * 4 + input_list


def initialize_q_state(word):
    return initialize_state(list(map(int, str(word))))


def gen_ndigit_num(length):
    if length == 1:
        yield from reversed(range(1, 10))
    elif length > 1:
        for i in reversed(range(1, 10)):
            for num in gen_ndigit_num(length - 1):
                yield i * 10 ** (length - 1) + num


def get_solution():
    with open('input/day24_input.txt') as f:
        lines = f.readlines()
    lines1 = '''inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2'''.splitlines()
    program = [parse_line(line.strip()) for line in lines]
    print(run_program(program, initialize_q_state(59998426997979)))
    print(run_program(program, initialize_q_state(13621111481315)))
    # for num in gen_ndigit_num(14): this will be too slow
    #     result = run_program(program, initialize_q_state(num))
    #     if result[3] == 0:
    #         print(result)
    #         break

    # symbolically executing the program, we find the following constraints for z = 0 at the end:
    # w[4] = w[3] - 1
    # w[5] = w[2] - 5
    # w[8] = w[7] + 3
    # w[9] = w[6] + 7
    # w[11] = w[10] + 2
    # w[12] = w[1] - 2
    # w[13] = w[0] + 4
    #
    # making the answers:
    # 59998426997979
    # 13621111481315
