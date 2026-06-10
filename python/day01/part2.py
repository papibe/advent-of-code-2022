def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        raw_data: str = fp.read()

    # set initial values for 3 maxs
    max_calories_1: int = 0
    max_calories_2: int = 0
    max_calories_3: int = 0

    for elf_snack_calories in raw_data.split("\n\n"):
        total_elf_calories: int = sum(
            [int(calorie) for calorie in elf_snack_calories.splitlines()]
        )

        # update max values if necessary
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


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 24000

    result = solution("./input.txt")
    print(result)
