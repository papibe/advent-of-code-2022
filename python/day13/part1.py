from typing import List
from ast import literal_eval


def is_right_order(left: List, right: List, index: int) -> bool:
    print(f"---{left}, {right}, {index}")

    if index >= len(left) and index >= len(right):
        return None
    if index >= len(left):
        return True
    if index >= len(right):
        return False

    print(f"Compare {left[index]} vs {right[index]}")

    if isinstance(left[index], list) and isinstance(right[index], list):
        return is_right_order(left[index], right[index], 0)

    if isinstance(left[index], int) and isinstance(right[index], int):
        if left[index] < right[index]:
            return True
        elif left[index] > right[index]:
            return False
        else:
            result = is_right_order(left, right, index + 1)
            if result is None:
                print(f"what to do with ---{left}, {right}, {index}")
            else:
                return result


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().split("\n\n")

    # parse data
    pair_of_packets: List[List] = []
    for pair in data:
        packages: List[List] = [literal_eval(package) for package in pair.splitlines()]
        # print(packages)
        pair_of_packets.append(packages)

    # compare each par
    right_order_indexes: List[int] = []
    for index, pair in enumerate(pair_of_packets):
        left_package, right_package = pair
        # print(left_package, right_package)
        if is_right_order(left_package, right_package, 0):
            print(index + 1, "true")
            right_order_indexes.append(index + 1)

    print(right_order_indexes)

    return sum(right_order_indexes)


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)
