from ast import literal_eval
from dataclasses import dataclass
from typing import List

type Package = List[Package] | int


@dataclass
class Packages:
    left: Package
    right: Package


def parse(filename: str) -> List[Packages]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().split("\n\n")

    packets: List[Packages] = []
    for pair in data:
        packages_line: List[str] = pair.splitlines()
        left_package: Package = literal_eval(packages_line[0])
        right_package: Package = literal_eval(packages_line[1])

        package_pair: Packages = Packages(left_package, right_package)
        packets.append(package_pair)

    return packets


def is_right_order(left: Package, right: Package) -> bool | None:
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


def solve(packets: List[Packages]) -> int:
    right_order_indexes: List[int] = []

    for index, pair in enumerate(packets, start=1):
        if is_right_order(pair.left, pair.right):
            right_order_indexes.append(index)

    return sum(right_order_indexes)


def solution(filename: str) -> int:
    packages: List[Packages] = parse(filename)
    return solve(packages)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 13
    print(solution("./input.txt"))  # 5905
