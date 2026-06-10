def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        raw_data: str = fp.read()

    max_calories: int = 0
    for elf_snack_calories in raw_data.split("\n\n"):
        total_elf_calories: int = sum(
            [int(calorie) for calorie in elf_snack_calories.splitlines()]
        )
        max_calories = max(max_calories, total_elf_calories)

    return max_calories


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 24000

    result = solution("./input.txt")
    print(result)
