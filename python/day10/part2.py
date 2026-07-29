import re
from collections import namedtuple
from typing import List, Match, Optional, Set

CYCLES: Set[int] = {20, 60, 100, 140, 180, 220}

Instruction = namedtuple("Instruction", ["type", "param"])


def parse(filename: str) -> List[Instruction]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    instructions: List[Instruction] = []
    for line in data:
        if line == "noop":
            instructions.append(Instruction("noop", 0))
        else:
            matches: Optional[Match[str]] = re.match(r"^addx ([0-9\-]+)", line)
            if matches:
                value: int = int(matches.group(1))
                instructions.append(Instruction("addx", value))

    return instructions


def print_display(display: List[str]) -> None:
    row_length: int = 40
    for index, bit in enumerate(display):
        if index % row_length == 0:
            print()
        print(bit, end="")
    print()


def solve(instructions: List[Instruction]) -> None:
    cycle: int = 1
    sprite: int = 1  # former x_register
    display: List[str] = [" " for _ in range(240)]
    display_position: int = 0

    for instr in instructions:
        display_position = (cycle - 1) % 40
        if sprite - 1 <= display_position <= sprite + 1:
            display[cycle - 1] = "#"
        else:
            display[cycle - 1] = "."

        match instr.type:
            case "noop":
                cycle += 1

            case "addx":
                cycle += 1
                display_position = (cycle - 1) % 40
                if sprite - 1 <= display_position <= sprite + 1:
                    display[cycle - 1] = "#"
                else:
                    display[cycle - 1] = "."

                sprite += instr.param
                cycle += 1

    print_display(display)


def solution(filename: str) -> None:
    instructions: List[Instruction] = parse(filename)
    solve(instructions)


if __name__ == "__main__":
    solution("./example.txt")
    solution("./input.txt")
