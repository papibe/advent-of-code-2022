from typing import List


def is_contained(fi: str, fe: str, si: str, se: str) -> bool:
    return (int(fi) <= int(si) and int(se) <= int(fe)) or (
        int(si) <= int(fi) and int(fe) <= int(se)
    )


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        section_pairs: List = fp.read().splitlines()

    fully_contained: int = 0
    for pair in section_pairs:
        first_pair, second_pair = pair.split(",")
        first_init, first_end = first_pair.split("-")
        second_init, second_end = second_pair.split("-")

        if is_contained(first_init, first_end, second_init, second_end):
            fully_contained += 1

    return fully_contained


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 2

    result = solution("./input.txt")
    print(result)
