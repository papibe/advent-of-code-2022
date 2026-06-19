from typing import List


def parse(filename: str) -> List[List[int]]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().split("\n\n")

    elf_calories: List[List[int]] = []
    for elf_block in data:
        str_calories: List[str] = elf_block.splitlines()
        elf_calories.append([int(calorie) for calorie in str_calories])

    return elf_calories


def solve(elf_calories: List[List[int]]) -> int:
    max_calories_1: int = 0
    max_calories_2: int = 0
    max_calories_3: int = 0

    for elf_snack_calories in elf_calories:
        total_elf_calories: int = sum(elf_snack_calories)

        # update max values
        if total_elf_calories > max_calories_1:
            max_calories_3 = max_calories_2
            max_calories_2 = max_calories_1
            max_calories_1 = total_elf_calories
        elif total_elf_calories > max_calories_2:
            max_calories_3 = max_calories_2
            max_calories_2 = total_elf_calories
        elif total_elf_calories > max_calories_3:
            max_calories_3 = total_elf_calories

    return max_calories_1 + max_calories_2 + max_calories_3


def solution(filename: str) -> int:
    elf_calories: List[List[int]] = parse(filename)
    return solve(elf_calories)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 45000
    print(solution("./input.txt"))  # 199628
