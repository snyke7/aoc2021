from typing import List
from math import prod as product

from parsy import generate, char_from, string
import attr


binary_digit = char_from('01')


def raw_binary_string(length):
    return binary_digit.times(length).concat()


def binary_string(length):
    return raw_binary_string(length).map(lambda num: int(num, 2))


@attr.s(auto_attribs=True)
class Packet:
    version: int

    def get_value(self):
        raise NotImplementedError


@attr.s(auto_attribs=True)
class LiteralPacket(Packet):
    value: int

    def get_value(self):
        return self.value


@attr.s(auto_attribs=True)
class OperatorPacket(Packet):
    operator_id: int
    packet_list: List[Packet]

    def get_value(self):
        packet_vals_iter = (packet.get_value() for packet in self.packet_list)
        if self.operator_id == 0:
            return sum(packet_vals_iter)
        elif self.operator_id == 1:
            return product(packet_vals_iter)
        elif self.operator_id == 2:
            return min(packet_vals_iter)
        elif self.operator_id == 3:
            return max(packet_vals_iter)
        elif self.operator_id == 5:
            return 1 if self.packet_list[0].get_value() > self.packet_list[1].get_value() else 0
        elif self.operator_id == 6:
            return 1 if self.packet_list[0].get_value() < self.packet_list[1].get_value() else 0
        elif self.operator_id == 7:
            return 1 if self.packet_list[0].get_value() == self.packet_list[1].get_value() else 0


def parse_literal(version, read_more=True):
    @generate
    def parse_fn():
        hex_len = 6
        read_next = True
        literal_bit_str = ''
        while read_next:
            bit_read_next = yield binary_string(1)
            read_next = bit_read_next == 1
            bits_of_str = yield raw_binary_string(4)
            literal_bit_str += bits_of_str
            hex_len += 5
        # read trailing zeroes
        if read_more and hex_len % 4:
            yield string('0').times(4 - (hex_len % 4))
        return LiteralPacket(version, int(literal_bit_str, 2))
    return parse_fn


def parse_operator(version, operator):
    @generate
    def parse_fn():
        length_type_bit = yield binary_string(1)
        if length_type_bit == 0:
            sub_packets_len = yield binary_string(15)
            sub_packets_data = yield raw_binary_string(sub_packets_len)
            packets = parse_packet(False).many().parse(sub_packets_data)
            return OperatorPacket(version, operator, packets)
        else:
            num_packets = yield binary_string(11)
            packets = yield parse_packet(False).times(num_packets)
            return OperatorPacket(version, operator, packets)
    return parse_fn


def parse_packet(read_more=True):
    @generate
    def parse_fn():
        version = yield binary_string(3)
        type_id = yield binary_string(3)
        if type_id == 4:
            result = yield parse_literal(version, read_more=read_more)
        else:
            result = yield parse_operator(version, type_id)
        return result
    return parse_fn


def hex_to_binary(num_str):
    num_bins = len(num_str) * 4
    fmt = f'{{0:0{num_bins}b}}'
    return fmt.format(int(num_str, 16))


def get_version_sum(packet: Packet):
    the_sum = packet.version
    if isinstance(packet, OperatorPacket):
        for sub_pack in packet.packet_list:
            the_sum += get_version_sum(sub_pack)
    return the_sum


parse_packet_total = parse_packet() << string('0').many()


def get_solution():
    with open('input/day16_input.txt') as f:
        lines = ''.join(f.readlines()).strip()
    lines1 = 'D2FE28'
    lines2 = '38006F45291200'
    lines3 = 'EE00D40C823060'
    lines4 = '8A004A801A8002F478'
    lines5 = '620080001611562C8802118E34'
    lines6 = 'C0015000016115A2E0802F182340'
    lines7 = 'A0016C880162017C3686B18A3D4780'
    lines8 = 'C200B40A82'
    lines9 = '04005AC33890'
    lines10 = '880086C3E88112'
    lines11 = 'CE00C43D881120'
    lines12 = 'D8005AC2A8F0'
    lines13 = 'F600BC2D8F'
    lines14 = '9C005AC2F8F0'
    lines15 = '9C0141080250320F1802104A08'
    binary_input = hex_to_binary(lines)
    result = parse_packet_total.parse(binary_input)
    print(get_version_sum(result))
    print(result.get_value())
