from typing import List


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        rucksacks: List = fp.read().splitlines()

    priority_sum: int = 0
    index: int = 0
    while index < len(rucksacks):
        elf_1: set = set(rucksacks[index])
        elf_2: set = set(rucksacks[index + 1])
        elf_3: set = set(rucksacks[index + 2])

        for item in elf_1 & elf_2 & elf_3:
            if item.islower():
                priority_sum += ord(item) - ord("a") + 1
            else:
                priority_sum += ord(item) - ord("A") + 27

        index += 3

    return priority_sum


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 70

    result = solution("./input.txt")
    print(result)
