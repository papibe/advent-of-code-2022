from typing import List
from ast import literal_eval


def is_right_order(left: List, right: List) -> bool:

    print(f"Compare {left} vs {right}")

    if isinstance(left, list) and isinstance(right, list):
        print(f"list vs list")
        index = 0
        while True:
            print(f"{index = }")
            if index >= len(left) and index >= len(right):
                return None
            if index >= len(left):
                return True
            if index >= len(right):
                return False

            result = is_right_order(left[index], right[index])
            if result is None:
                index += 1
            else:
                return result

        print("what2")

    if isinstance(left, int) and isinstance(right, int):
        print("int vs int")
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

    print("what!!!")


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
        if is_right_order(left_package, right_package):
            print(f"pair {index + 1} True")
            right_order_indexes.append(index + 1)
        else:
            print(f"pair {index + 1} False")

        print("==============================\n")

    print(right_order_indexes)

    return sum(right_order_indexes)


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)

    result: int = solution("./input.txt")
    print(result)
