from typing import List


def overlaps(fi: str, fe: str, si: str, se: str) -> bool:
    if fe < si or se < fi:
        return False
    else:
        return True


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        section_pairs: List = fp.read().splitlines()

    total_overlaps: int = 0
    for pair in section_pairs:
        first_pair, second_pair = pair.split(",")
        first_init, first_end = first_pair.split("-")
        second_init, second_end = second_pair.split("-")

        if overlaps(int(first_init), int(first_end), int(second_init), int(second_end)):
            total_overlaps += 1

    return total_overlaps


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 4

    result = solution("./input.txt")
    print(result)
