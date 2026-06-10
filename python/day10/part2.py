import re
import math
from typing import List, Set, Tuple

CYCLES = [20, 60, 100, 140, 180, 220]

def print_display(display: List[str]) -> None:
    row_length: int = 40
    for index, bit in enumerate(display):
        if index % row_length == 0:
            print()
        print(bit, end='')
    print()

def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        program: List[str] = fp.read().splitlines()

    cycle: int = 1
    sprite: int = 1 # former x_register
    display: List[str] = [' ' for _ in range(240)]
    display_position: int = 0

    for line in program:
        print(cycle, sprite)
        display_position = (cycle - 1) % 40
        if sprite - 1 <= display_position <= sprite + 1:
            display[cycle - 1] = '#'
        else:
            display[cycle - 1] = '.'

        if line.startswith("noop"):
            cycle += 1
            continue

        expr = re.match("^addx ([0-9\-]+)", line)
        value = int(expr.group(1))
        cycle += 1
        print(cycle, sprite)
        display_position = (cycle - 1) % 40
        if sprite - 1 <= display_position <= sprite + 1:
            display[cycle - 1] = '#'
        else:
            display[cycle - 1] = '.'

        sprite += value
        cycle += 1

    print_display(display)

    return 0

if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 13140

    result = solution("./input.txt")
    print(result)
