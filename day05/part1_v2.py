import re
from typing import List


def solution(filename: str) -> str:
    with open(filename, "r") as fp:
        raw_data: str = fp.read()

    stacks_data, instructions = raw_data.split("\n\n")
    stacks_matrix: List[str] = stacks_data.splitlines()

    stacks: List = []
    number_of_rows: int = len(stacks_matrix)
    number_of_cols: int = len(stacks_matrix[0])

    # traverse last row
    for col in range(number_of_cols):

        # if we found a number go up the column to create a list
        if stacks_matrix[-1][col].isnumeric():
            new_stack_row = []
            for row in range(number_of_rows - 2, -1, -1):
                # skip spaces
                if stacks_matrix[row][col] != " ":
                    new_stack_row.append(stacks_matrix[row][col])
            stacks.append(new_stack_row)

    for instruction in instructions.splitlines():
        move_data = re.match("move (\d+) from (\d+) to (\d+)", instruction)

        number_of_crates: int = int(move_data.group(1))
        source: int = int(move_data.group(2))
        destination: int = int(move_data.group(3))

        # move creates
        for _ in range(number_of_crates):
            stacks[destination - 1].append(stacks[source - 1].pop())

    message: List[str] = [row[-1] for row in stacks]

    return "".join(message)


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be "CMZ"

    result: int = solution("./input.txt")
    print(result)
