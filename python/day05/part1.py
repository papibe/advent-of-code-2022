import re
from collections import namedtuple
from typing import Dict, List, Match, Optional, Tuple

LAST: int = -1

Instruction = namedtuple("Instruction", ["source", "destination", "quantity"])
Stack = Dict[str, List[str]]


def parse(filename: str) -> Tuple[Stack, List[Instruction]]:
    with open(filename, "r") as fp:
        raw_data: str = fp.read()

    stacks_data, instructions_data = raw_data.split("\n\n")
    stack_lines: List[str] = stacks_data.splitlines()

    number_of_rows: int = len(stack_lines)

    stacks: Dict[str, List[str]] = {}

    for match in re.finditer(r"\d", stack_lines[LAST]):
        matched_text = match.group()
        start_index = match.start()
        stacks[matched_text] = [
            stack_lines[i][start_index]
            for i in range(number_of_rows - 2, -1, -1)
            if stack_lines[i][start_index] != " "
        ]

    instructions: List[Instruction] = []

    for instruction in instructions_data.splitlines():
        move_data: Optional[Match[str]] = re.match(
            r"move (\d+) from (\d+) to (\d+)", instruction
        )

        if move_data is not None:

            number_of_crates: int = int(move_data.group(1))
            source: str = move_data.group(2)
            destination: str = move_data.group(3)

            instructions.append(Instruction(source, destination, number_of_crates))

    return stacks, instructions


def solve(stacks: Stack, instructions: List[Instruction]) -> str:
    for instruction in instructions:
        for _ in range(instruction.quantity):
            stacks[instruction.destination].append(stacks[instruction.source].pop())

    message: List[str] = [row[LAST] for row in stacks.values()]
    return "".join(message)


def solution(filename: str) -> str:
    stacks, instructions = parse(filename)
    return solve(stacks, instructions)


if __name__ == "__main__":
    print(solution("./example.txt"))  # "CMZ"
    print(solution("./input.txt"))  # "MQTPGLLDN"
