from typing import Generator


raw_data = """38006F45291200"""

translator_table = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def from_binary_to_decimal(binary):
    return sum(int(b) * pow(2, i) for i, b in enumerate(reversed(binary)))


def read_n_bits(generator, n):
    return "".join(next(generator) for _ in range(n))


def hexa_to_bits(packet: str):
    for l in packet:
        bits = translator_table[l]
        for b in bits:
            yield b


def read_literal_value(generator, remove_extra_zeros):
    packet = ""
    continue_reading = True
    count = 6
    extra_bits = 0
    while continue_reading:
        prefix = next(generator)
        packet += read_n_bits(generator, 4)
        continue_reading = prefix == "1"
        extra_bits += 1
        count += 5

    if remove_extra_zeros:
        null_bits = 4 * (int(count / 4) + 1) - count
        read_n_bits(generator, null_bits)
        extra_bits += null_bits

    return packet, extra_bits


def read_from_length(generator, length, is_sub_packet):
    count = 0
    packets = []
    while count < length:
        packets.append(Packet(generator, is_sub_packet))
        count += packets[-1].get_length()
    return packets


def read_from_number(generator, n):
    packets = []
    while len(packets) < n:
        packets.append(Packet(generator, False))
    return packets


def read_operator(generator):
    length_type_id = int(next(generator))
    if length_type_id == 0:
        total_length = from_binary_to_decimal(read_n_bits(generator, 15))
        return read_from_length(generator, total_length, True), 16

    number_of_sub_packets = from_binary_to_decimal(read_n_bits(generator, 11))
    return read_from_number(generator, number_of_sub_packets), 12


class Packet:
    def __init__(self, bits: Generator, is_sub_packet):
        self.bits = bits
        self.version = read_n_bits(bits, 3)
        self.type_id = read_n_bits(bits, 3)
        self.content, self.extra_bits = self.parse(not is_sub_packet)

    def parse(self, remove_extra_zeros):
        if self.type_id == "100":
            return read_literal_value(self.bits, remove_extra_zeros)
        return read_operator(self.bits)

    def get_length(self):
        extra_length = 6 + self.extra_bits
        if self.type_id == "100":
            return extra_length + len(self.content)
        else:
            return extra_length + sum(p.get_length() for p in self.content)

    def extract_packets(self):
        if self.type_id == "100":
            return [self]
        else:
            sub_packets = []
            for p in self.content:
                sub_packets.extend(p.extract_packets())
            return sub_packets


class HexaParser:
    def __init__(self, hexa_line: str):
        self.packets = []
        self.length = len(hexa_line) * 4
        self.bits = hexa_to_bits(hexa_line)

    def parse(self):
        self.packets = read_from_length(self.bits, self.length, False)

    def get_all_packets(self):
        for p in self.packets:
            for sub_packet in p.extract_packets():
                yield sub_packet


def part1():
    parser = HexaParser(raw_data)
    parser.parse()
    all_versions = (p.version for p in parser.get_all_packets())
    decimal_versions = map(from_binary_to_decimal, all_versions)
    return sum(decimal_versions)


def part2():
    pass


if __name__ == "__main__":
    print(part1())
    print(part2())
