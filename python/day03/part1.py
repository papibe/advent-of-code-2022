from typing import List, Set


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        rucksacks: List[str] = fp.read().splitlines()

    return rucksacks


def solve(rucksacks: List[str]) -> int:
    priority_sum: int = 0
    for rucksack in rucksacks:
        compartment_1: Set[str] = set(rucksack[0 : len(rucksack) // 2])
        compartment_2: Set[str] = set(rucksack[len(rucksack) // 2 :])

        for item in compartment_1 & compartment_2:
            if item.islower():
                priority_sum += ord(item) - ord("a") + 1
            else:
                priority_sum += ord(item) - ord("A") + 27

    return priority_sum


def solution(filename: str) -> int:
    rucksacks: List[str] = parse(filename)
    return solve(rucksacks)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 157
    print(solution("./input.txt"))  # 8515
