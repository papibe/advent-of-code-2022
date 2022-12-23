from typing import List
from ast import literal_eval


class Packet:
    def __init__(self, str_list: str) -> None:
        self.value: List = literal_eval(str_list)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return is_right_order(self.value, other.value)

    def __repr__(self) -> str:
        return f"{self.value}"


def is_right_order(left: List, right: List) -> bool:
    # int vs int
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None

    # list vs list
    if isinstance(left, list) and isinstance(right, list):
        index = 0
        for index in range(max(len(left), len(right)) + 1):
            # index checking
            if index >= len(left) and index >= len(right):
                return None
            if index >= len(left):
                return True
            if index >= len(right):
                return False

            # check each element
            deeper_check = is_right_order(left[index], right[index])
            if deeper_check is not None:
                return deeper_check

            index += 1

    # int vs list
    if isinstance(left, int):
        return is_right_order([left], right)
    else:
        return is_right_order(left, [right])


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    # parse data and create list of packets
    packets: List[List] = []
    for str_packet in data:
        if str_packet == "":
            continue
        # print(packages)
        packets.append(Packet(str_packet))

    # add divider packets
    packets.append(Packet("[[2]]"))
    packets.append(Packet("[[6]]"))

    packets.sort()

    # search for divider packages
    for index, packet in enumerate(packets):
        packet_list: List = packet.value
        if (
            len(packet_list) == 1
            and isinstance(packet_list[0], list)
            and len(packet_list[0]) == 1
        ):
            if packet_list[0][0] == 2:
                divider_2_index = index + 1
            elif packet_list[0][0] == 6:
                divider_6_index = index + 1

    return divider_2_index * divider_6_index


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)

    result = solution("./input.txt")
    print(result)
