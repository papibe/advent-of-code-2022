import re
import math
from typing import List, Set, Tuple

CYCLES = [20, 60, 100, 140, 180, 220]


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        program: List[str] = fp.read().splitlines()

    cycle: int = 1
    x_register: int = 1
    signal_strength: int = 0
    for line in program:
        if cycle in CYCLES:
            print(cycle, x_register, cycle * x_register)
            signal_strength += cycle * x_register

        if line.startswith("noop"):
            cycle += 1
            continue

        expr = re.match("^addx ([0-9\-]+)", line)
        value = int(expr.group(1))
        cycle += 1
        if cycle in CYCLES:
            print(cycle, x_register, cycle * x_register)
            signal_strength += cycle * x_register

        x_register += value
        cycle += 1

    return signal_strength

if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 13140

    result = solution("./input.txt")
    print(result)
