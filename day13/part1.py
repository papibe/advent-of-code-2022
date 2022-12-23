from typing import List
from ast import literal_eval


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
        data: List[str] = fp.read().split("\n\n")

    # parse data and create list of packets
    pair_of_packets: List[List] = []
    for pair in data:
        packages: List[List] = [literal_eval(package) for package in pair.splitlines()]
        pair_of_packets.append(packages)

    # compare each par
    right_order_indexes: List[int] = []
    for index, pair in enumerate(pair_of_packets):
        left_package, right_package = pair

        if is_right_order(left_package, right_package):
            right_order_indexes.append(index + 1)

    return sum(right_order_indexes)


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)

    result = solution("./input.txt")
    print(result)
