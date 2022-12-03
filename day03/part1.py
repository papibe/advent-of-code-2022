from typing import List


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        rucksacks: List = fp.read().splitlines()

    priority_sum: int = 0
    for rucksack in rucksacks:
        compartment_1: set = set(rucksack[0 : len(rucksack) // 2])
        compartment_2: set = set(rucksack[len(rucksack) // 2 :])

        for item in compartment_1 & compartment_2:
            if item.islower():
                priority_sum += ord(item) - ord("a") + 1
            else:
                priority_sum += ord(item) - ord("A") + 27

    return priority_sum


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 157

    result: int = solution("./input.txt")
    print(result)
