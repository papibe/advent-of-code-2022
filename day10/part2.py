import re
from typing import List

CYCLES = [20, 60, 100, 140, 180, 220]


def build_display_output(display: List[str], row_length: int) -> str:
    output: List[str] = []

    for index, bit in enumerate(display):
        if index % row_length == 0:
            output.append("\n")
        output.append(bit)
    output.append("\n")

    return "".join(output)


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        program: List[str] = fp.read().splitlines()

    cycle: int = 1
    sprite: int = 1  # former x_register
    display: List[str] = [" " for _ in range(240)]
    display_position: int = 0

    for line in program:
        display_position = (cycle - 1) % 40
        if sprite - 1 <= display_position <= sprite + 1:
            display[cycle - 1] = "#"
        else:
            display[cycle - 1] = "."

        if line.startswith("noop"):
            cycle += 1
            continue

        expr = re.match("^addx ([0-9\-]+)", line)
        value = int(expr.group(1))
        cycle += 1

        display_position = (cycle - 1) % 40
        if sprite - 1 <= display_position <= sprite + 1:
            display[cycle - 1] = "#"
        else:
            display[cycle - 1] = "."

        sprite += value
        cycle += 1

    return build_display_output(display, 40)


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # see README.md for expected output

    result = solution("./input.txt")
    print(result)
