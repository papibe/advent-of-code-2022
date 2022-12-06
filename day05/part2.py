import re
from typing import List


def solution(filename: str) -> str:
    with open(filename, "r") as fp:
        raw_data: str = fp.read()

    stacks_data, instructions = raw_data.split("\n\n")
    stacks_matrix: List[List] = [list(row) for row in stacks_data.splitlines()]

    stacks: List[List] = []

    for row in [*zip(*stacks_matrix)]:
        if row[-1].isnumeric():
            stacks.append(list("".join(reversed(list(row))).strip())[1:])

    for instruction in instructions.splitlines():
        move_data = re.match("move (\d+) from (\d+) to (\d+)", instruction)
        number_of_crates: int = int(move_data.group(1))
        source: int = int(move_data.group(2))
        destination: int = int(move_data.group(3))

        # move crates
        stack_hight: int = len(stacks[source - 1])
        crates_to_move: List[str] = stacks[source - 1][-number_of_crates:]
        stacks[source - 1] = stacks[source - 1][: stack_hight - number_of_crates]
        stacks[destination - 1].extend(crates_to_move)

    message: List[str] = [row[-1] for row in stacks]

    return "".join(message)


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 2

    result: int = solution("./input.txt")
    print(result)
