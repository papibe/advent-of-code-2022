from enum import Enum, auto
from typing import List, Tuple, Dict


class Direction(Enum):
    right: str = auto()
    left: str = auto()
    up: str = auto()
    down: str = auto()


class Board:
    def __init__(self, board_map: List[str]) -> None:
        self.map: List[str] = board_map

        limits: Dict[int, Tuple[int, int]] = {}
        for row_number, row in enumerate(board_map):
            min_col = len(row) - len(row.strip())
            max_col = len(row)
            print(row_number, row, min_col, max_col)
            limits[row_number] = (min_col, max_col)

        self.limits: Dict[int, Tuple[int, int]] = limits

    def get_start_position(self) -> Tuple[int, int]:
        return (0, self.limits[0][0])

    def get(self, row: int, col: int) -> str:
        return self.map[row][col]

    def move(self, current, next_) -> Tuple:
        pass


def parse(filename: str) -> Tuple[List[str], str]:
    with open(filename, "r") as fp:
        data: str = fp.read()

    str_board_map, str_path_instructions = data.split("\n\n")
    board_map: List[str] = str_board_map.splitlines()
    path_instructions: List[str] = str_path_instructions[:-1]

    return Board(board_map), path_instructions


def parse_instructions(str_instructions: str) -> List[str]:
    """this works but it is horrible"""

    tmp_instructions: List = []

    r_split = str_instructions.split("R")
    for i in range(len(r_split) - 1):
        tmp_instructions.append(r_split[i])
        tmp_instructions.append("R")
    tmp_instructions.append(r_split[-1])

    final_instructions: List = []
    for item in tmp_instructions:
        l_split = item.split("L")
        if len(l_split) == 1:
            final_instructions.append(item)
        else:
            for i in range(len(l_split) - 1):
                final_instructions.append(l_split[i])
                final_instructions.append("L")
            final_instructions.append(l_split[-1])

    # if str_instructions != "".join(final_instructions):
    #     print("problem!!")

    return final_instructions


def rotate(facing: str, instruction: str) -> str:
    rotation_rules: Dict = {
        Direction.right: {
            "R": Direction.down,
            "L": Direction.up,
        },
        Direction.left: {
            "R": Direction.up,
            "L": Direction.down,
        },
        Direction.up: {
            "R": Direction.right,
            "L": Direction.left,
        },
        Direction.down: {
            "R": Direction.left,
            "L": Direction.right,
        },
    }
    return rotation_rules[facing][instruction]


def move(
    position: Tuple[int, int], direction: str, board_map: List[str], steps: int
) -> Tuple[int, int]:
    space_increment: Dict = {
        Direction.right: (0, 1),
        Direction.left: (0, -1),
        Direction.up: (-1, 0),
        Direction.down: (1, 0),
    }
    for _ in range(steps):
        pos_row, pos_col = position
        next_pos_row, next_pos_col = (
            pos_row + space_increment[direction][0],
            pos_col + space_increment[direction][1],
        )
        next_position = board_map.move(
            (next_pos_row, next_pos_col), board_map.get(next_pos_row, next_pos_col)
        )
        if next_position == position:
            print(f"{position = }")
            return position
        position = next_position

    print(f"{position = }")
    return position


def solve(board_map: List[str], path: str) -> int:
    facing: str = Direction.right
    current_position: Tuple[int, int] = board_map.get_start_position()
    # print(current_position)
    # print(board_map[current_position[0]][current_position[1]])

    for instruction in path:
        if instruction in ["L", "R"]:
            facing = rotate(facing, instruction)
            continue
        steps = int(instruction)
        current_position = move(current_position, facing, board_map, steps)

        # DEBUG
        return 0

    return 0


def solution(filename: str):
    board_map, raw_path_instructions = parse(filename)
    path_instructions: List = parse_instructions(raw_path_instructions)
    return solve(board_map, path_instructions)


if __name__ == "__main__":
    print(solution("./example.txt"))
    # print(solution("./input.txt"))
