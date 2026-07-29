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


def solve(instructions: List[Instruction]) -> int:
    cycle: int = 1
    x_register: int = 1
    signal_strength: int = 0

    for instr in instructions:
        if cycle in CYCLES:
            signal_strength += cycle * x_register

        match instr.type:
            case "noop":
                cycle += 1

            case "addx":
                cycle += 1
                if cycle in CYCLES:
                    signal_strength += cycle * x_register

                x_register += instr.param
                cycle += 1

    return signal_strength


def solution(filename: str) -> int:
    instructions: List[Instruction] = parse(filename)
    return solve(instructions)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 13140
    print(solution("./input.txt"))  # 13180
