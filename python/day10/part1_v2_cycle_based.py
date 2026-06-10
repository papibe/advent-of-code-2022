import re
from enum import Enum
from typing import List, Tuple, Optional

CYCLES = [20, 60, 100, 140, 180, 220]


class Instruction(Enum):
    NOOP = "noop"
    ADDX = "addx"
    END_PROGRAM = "end"


def get_instruction(
    program: List[str], index: int
) -> Tuple[Instruction, Optional[int]]:

    if index >= len(program):
        return Instruction.END_PROGRAM, None

    if program[index].startswith(Instruction.NOOP.value):
        return Instruction.NOOP, None

    expr = re.match("^addx (-*\d+)", program[index])
    return Instruction.ADDX, int(expr.group(1))


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        program: List[str] = fp.read().splitlines()

    cycle: int = 1
    x_register: int = 1
    signal_strength: int = 0
    instruction_index: int = 0
    is_simple_cycle: bool = True

    while cycle <= CYCLES[-1]:  # 220
        if is_simple_cycle:
            instruction, value = get_instruction(program, instruction_index)

            if instruction == Instruction.END_PROGRAM:
                break
            instruction_index += 1

            if instruction != Instruction.NOOP:
                is_simple_cycle = False
        else:
            x_register += value
            is_simple_cycle = True

        cycle += 1
        if cycle in CYCLES:
            signal_strength += cycle * x_register

    return signal_strength


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 13140

    result = solution("./input.txt")
    print(result)
