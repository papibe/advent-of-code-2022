from ast import literal_eval
from typing import List

type Packet_Item = List[Packet_Item] | List[int] | int
type Package_List = List[Packet_Item]


class Packet:
    def __init__(self, str_list: str) -> None:
        self.value: Package_List = literal_eval(str_list)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Packet):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other: "Packet") -> bool | None:
        return is_right_order(self.value, other.value)

    def __repr__(self) -> str:
        return f"{self.value}"


def parse(filename: str) -> List[Packet]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().split("\n\n")

    packets: List[Packet] = []
    for pair in data:
        packages_line: List[str] = pair.splitlines()
        packets.append(Packet(packages_line[0]))
        packets.append(Packet(packages_line[1]))

    return packets


def is_right_order(left: Packet_Item, right: Packet_Item) -> bool | None:
    # both lists
    if isinstance(left, list) and isinstance(right, list):
        index: int = 0
        while True:
            if index >= len(left) and index >= len(right):
                return None
            if index >= len(left):
                return True
            if index >= len(right):
                return False

            result: bool | None = is_right_order(left[index], right[index])
            if result is None:
                index += 1
            else:
                return result

    # both ints
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None

    if isinstance(left, int):
        return is_right_order([left], right)

    if isinstance(right, int):
        return is_right_order(left, [right])

    return None


def solve(packets: List[Packet]) -> int:
    # patch list of packets
    first_packet: Packet = Packet("[[2]]")
    second_packet: Packet = Packet("[[6]]")

    packets.append(first_packet)
    packets.append(second_packet)

    packets.sort()
    # packets = sorted(packets)

    # search for divider packages
    for index, packet in enumerate(packets, start=1):
        if packet == first_packet:
            divider_2_index = index

        elif packet == second_packet:
            divider_6_index = index

    return divider_2_index * divider_6_index


def solution(filename: str) -> int:
    packages: List[Packet] = parse(filename)
    return solve(packages)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 140
    print(solution("./input.txt"))  # 21691
