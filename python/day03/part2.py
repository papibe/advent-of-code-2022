from typing import List, Set


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        rucksacks: List[str] = fp.read().splitlines()

    return rucksacks


def solve(rucksacks: List[str]) -> int:
    priority_sum: int = 0
    index: int = 0
    while index < len(rucksacks):
        elf_1: Set[str] = set(rucksacks[index])
        elf_2: Set[str] = set(rucksacks[index + 1])
        elf_3: Set[str] = set(rucksacks[index + 2])

        for item in elf_1 & elf_2 & elf_3:
            if item.islower():
                priority_sum += ord(item) - ord("a") + 1
            else:
                priority_sum += ord(item) - ord("A") + 27

        index += 3

    return priority_sum


def solution(filename: str) -> int:
    rucksacks: List[str] = parse(filename)
    return solve(rucksacks)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 70
    print(solution("./input.txt"))  # 2434
