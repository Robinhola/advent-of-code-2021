from typing import Generator


raw_data = """00537390040124EB240B3EDD36B68014D4C9ECCCE7BDA54E62522A300525813003560004223BC3F834200CC108710E98031C94C8B4BFFF42398309DDD30EEE00BCE63F03499D665AE57B698F9802F800824DB0CE1CC23100323610069D8010ECD4A5CE5B326098419C319AA2FCC44C0004B79DADB1EB48CE5EB7B2F4A42D9DF0AA74E66468C0139341F005A7BBEA5CA65F3976200D4BC01091A7E155991A7E155B9B4830056C01593829CC1FCD16C5C2011A340129496A7EFB3CA4B53F7D92675A947AB8A016CD631BE15CD5A17CB3CEF236DBAC93C4F4A735385E401804AA86802D291ED19A523DA310006832F07C97F57BC4C9BBD0764EE88800A54D5FB3E60267B8ED1C26AB4AAC0009D8400854138450C4C018855056109803D11E224112004DE4DB616C493005E461BBDC8A80350000432204248EA200F4148FD06C804EE1006618419896200FC1884F0A00010A8B315A129009256009CFE61DBE48A7F30EDF24F31FCE677A9FB018F6005E500163E600508012404A72801A4040688010A00418012002D51009FAA0051801CC01959801AC00F520027A20074EC1CE6400802A9A004A67C3E5EA0D3D5FAD3801118E75C0C00A97663004F0017B9BD8CCA4E2A7030C0179C6799555005E5CEA55BC8025F8352A4B2EC92ADF244128C44014649F52BC01793499EA4CBD402697BEBD18D713D35C9344E92CB67D7DFF05A60086001610E21A4DD67EED60A8402415802400087C108DB068001088670CA0DCC2E10056B282D6009CFC719DB0CD3980026F3EEF07A29900957801AB8803310A0943200042E3646789F37E33700BE7C527EECD13266505C95A50F0C017B004272DCE573FBB9CE5B9CAE7F77097EC830401382B105C0189C1D92E9CCE7F758B91802560084D06CC7DD679BC8048AF00400010884F18209080310FE0D47C94AA00"""
# raw_data = "A0016C880162017C3686B18A3D4780"
# raw_data = """C200B40A82"""
# raw_data = """04005AC33890"""
# raw_data = "880086C3E88112"
# raw_data = "CE00C43D881120"
# raw_data = "D8005AC2A8F0"
# raw_data = "F600BC2D8F"
# raw_data = "9C005AC2F8F0"
# raw_data = "9C0141080250320F1802104A08"

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


def read_literal_value(generator):
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

    return packet, extra_bits


def read_from_length(generator, length):
    count = 0
    packets = []
    while count < length:
        packets.append(Packet(generator))
        count += packets[-1].get_length()
    return packets


def read_from_number(generator, n):
    packets = []
    while len(packets) < n:
        packets.append(Packet(generator))
    return packets


def read_operator(generator):
    length_type_id = int(next(generator))
    if length_type_id == 0:
        total_length = from_binary_to_decimal(read_n_bits(generator, 15))
        return read_from_length(generator, total_length), 16

    number_of_sub_packets = from_binary_to_decimal(read_n_bits(generator, 11))
    return read_from_number(generator, number_of_sub_packets), 12


class Packet:
    def __init__(self, bits: Generator):
        self.bits = bits
        self.version = read_n_bits(bits, 3)
        self.type_id = from_binary_to_decimal(read_n_bits(bits, 3))
        self.content, self.extra_bits = self.parse()

    def parse(self):
        if self.type_id == 4:
            return read_literal_value(self.bits)
        return read_operator(self.bits)

    def get_length(self):
        extra_length = 6 + self.extra_bits
        if self.type_id == 4:
            return extra_length + len(self.content)
        else:
            return extra_length + sum(p.get_length() for p in self.content)

    def extract_packets(self):
        if self.type_id == 4:
            return [self]
        else:
            sub_packets = [self]
            for p in self.content:
                sub_packets.extend(p.extract_packets())
            return sub_packets

    def compute(self):
        values_of_sub_packets = (p.compute() for p in self.content)
        if self.type_id == 0:
            return sum(values_of_sub_packets)
        if self.type_id == 1:
            product = 1
            for value in values_of_sub_packets:
                product *= value
            return product

        if self.type_id == 2:
            return min(values_of_sub_packets)
        if self.type_id == 3:
            return max(values_of_sub_packets)

        if self.type_id == 4:
            return from_binary_to_decimal(self.content)

        if self.type_id == 5:
            return 1 if self.content[0].compute() > self.content[1].compute() else 0
        if self.type_id == 6:
            return 1 if self.content[0].compute() < self.content[1].compute() else 0
        if self.type_id == 7:
            return 1 if self.content[0].compute() == self.content[1].compute() else 0


class HexaParser:
    def __init__(self, hexa_line: str):
        bits = hexa_to_bits(hexa_line)
        self.packet = Packet(bits)

    def get_all_packets(self):
        for sub_packet in self.packet.extract_packets():
            yield sub_packet

    def compute(self):
        return self.packet.compute()


def part1():
    parser = HexaParser(raw_data)
    all_versions = (p.version for p in parser.get_all_packets())
    decimal_versions = map(from_binary_to_decimal, all_versions)
    return sum(decimal_versions)


def part2():
    parser = HexaParser(raw_data)
    return parser.compute()


if __name__ == "__main__":
    print(part1())
    print(part2())
