from enum import Enum, auto
from typing import List, Tuple, Dict, Iterator
from copy import deepcopy


class Direction(Enum):
    right: str = ">"
    left: str = "<"
    up: str = "^"
    down: str = "v"


class Board:
    def __init__(
        self, board_map: List[str], side: int, layout: List[str], stiches: Dict
    ) -> None:
        self.original_board = [list(row) for row in board_map]
        self.board = deepcopy(self.original_board)
        self.layout = layout
        self.side = side
        self.stiches = stiches
        self.start: Tuple[int, int] = (0, layout[0].count(" ") * side)

        face_position = {}
        for i, row in enumerate(self.layout):
            for j, face in enumerate(row):
                face_position[face] = (i, j)
        self.face_position = face_position

    def regen(self):
        self.board = deepcopy(self.original_board)

    def get_start(self) -> Tuple[int, int]:
        return self.start

    # def get(self, row: int, col: int) -> str:
    #     return self.start

    def move(self, current: Tuple[int, int], direction: Direction) -> Tuple:
        steps = {
            Direction.right: (0, 1),
            Direction.left: (0, -1),
            Direction.up: (-1, 0),
            Direction.down: (1, 0),
        }
        current_row, current_col = current
        row_step, col_step = steps[direction]
        next_row, next_col = (current_row + row_step, current_col + col_step)

        face_row = current_row // self.side
        face_col = current_col // self.side
        # print(f"{current_row = }, {current_col = }")
        # print(f"{face_row = }, {face_col = }")

        if (
            next_row < 0
            or next_row > len(self.board) - 1
            or next_col < 0
            or next_col > len(self.board[next_row]) - 1
            or self.board[next_row][next_col] == " "
        ):
            current_face = self.layout[face_row][face_col]
            # print(f"{current_face = }")
            if (
                current_face not in self.stiches
                or direction not in self.stiches[current_face]
            ):
                print(f"\n\nIncomplete stiches {current_face} {direction}\n\n")
                raise KeyError

            next_face, direction, row_func, col_func = self.stiches[current_face][
                direction
            ]
            # print(f"{col_func = }")
            current_face_row, current_face_col = self.face_position[current_face]
            # print(f"{current_face_row = }, {current_face_col = }")
            current_relative_row = current_row - current_face_row * self.side
            current_relative_col = current_col - current_face_col * self.side
            # print(f"{current_relative_row = } {current_relative_col = }")

            next_relative_row = (
                current_relative_row * row_func[0]
                + current_relative_col * row_func[1]
                + row_func[2]
            ) % self.side
            next_relative_col = (
                current_relative_row * col_func[0]
                + current_relative_col * col_func[1]
                + col_func[2]
            ) % self.side

            # current_face_row, current_face_col = self.face_position[current_face]
            next_face_row, next_face_col = self.face_position[next_face]
            # print(f"{next_face =}")
            next_row = next_relative_row + next_face_row * self.side
            next_col = next_relative_col + next_face_col * self.side

            # print(f"{next_relative_row = } {next_relative_col = }")
            # print(current_face, current, next_face, next_row, next_col)

        if self.board[next_row][next_col] != "#":
            return (next_row, next_col), direction
        else:
            return current, direction

    def print(self, position: Tuple[int, int], facing: Direction):
        for i, line in enumerate(self.board):
            for j, item in enumerate(line):
                if (i, j) == position:
                    print(facing.value, end="")
                else:
                    print(item, end="")
            print()
        print()


def parse(
    filename: str, side_side: int, layout: List[str], stiches
) -> Tuple[List[str], str]:
    with open(filename, "r") as fp:
        data: str = fp.read()

    str_board_map, str_path_instructions = data.split("\n\n")
    board_map: List[str] = str_board_map.splitlines()
    path_instructions: List[str] = str_path_instructions[:-1]

    return Board(board_map, side_side, layout, stiches), path_instructions


def parse_instructions(str_instructions: str) -> List:
    r_split: List = str_instructions.split("R")
    added_r: str = ",R,".join(r_split)
    l_split: List = added_r.split("L")
    added_both: str = ",L,".join(l_split)

    return added_both.split(",")


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


def solve(board_map: Board, path: str) -> int:
    facing: str = Direction.right
    current_position: Tuple[int, int] = board_map.get_start()
    # print(current_position)
    # return 0
    # print(board_map[current_position[0]][current_position[1]])

    # board_map.print(current_position, facing)

    counter: int = 0
    for instruction in path:
        if instruction in ["L", "R"]:
            facing = rotate(facing, instruction)
            print(f"new {facing = }")
            continue
        steps = int(instruction)
        print(f"{steps = }")
        for _ in range(steps):
            next_position, next_facing = board_map.move(current_position, facing)
            if next_position == current_position:
                break
            current_position = next_position
            facing = next_facing
            # board_map.print(current_position, facing)

        # DEBUG
        # counter += 1
        # if counter > 2:
        #     break

    direction_value: Dict[Direction, int] = {
        Direction.right: 0,
        Direction.left: 2,
        Direction.up: 3,
        Direction.down: 1,
    }

    current_row, current_col = current_position
    print(f"{current_row = }, {current_col = }, {direction_value[facing] = }")

    return 1_000 * (current_row + 1) + 4 * (current_col + 1) + direction_value[facing]


def solution2(filename: str, side_side: int, layout: List[str], stiches: Dict) -> int:
    board_map, raw_path_instructions = parse(filename, side_side, layout, stiches)
    path_instructions: List = parse_instructions(raw_path_instructions)
    # board_map.print()
    # return 0
    return solve(board_map, path_instructions)


def filler():
    letters: str = "abcdefghijklmnopqrstuvwxyz"
    pattern: str = letters  # + letters.upper()

    index: int = 0
    while True:
        yield pattern[index]
        index = (index + 1) % len(pattern)


# TODO: write test function
def test_stich_rule(board, origin_face, rule, direction, size):
    # print(f"{origin_face = }, {direction = } {rule = }")
    print(f"{origin_face = }, {direction = }")

    char_filler: Iterator = filler()

    adj_row, adj_col = 0, 0
    # print(rule)
    if direction in [Direction.up, Direction.down]:
        step = (0, 1)
    else:
        step = (1, 0)

    if direction == Direction.right:
        adj_col = size - 1
    if direction == Direction.down:
        adj_row = size - 1

    next_face, expected_next_direction, _, _ = rule
    step_row, step_col = step
    face_row, face_col = board.face_position[origin_face]
    row, col = adj_row + face_row * size, adj_col + face_col * size

    for index in range(size):
        cur_row, cur_col = (row + index * step_row, col + index * step_col)
        next_position, next_direction = board.move((cur_row, cur_col), direction)

        next_row, next_col = next_position
        # print((cur_row, cur_col), "->", next_position)
        char: str = next(char_filler)
        board.board[cur_row][cur_col] = char
        board.board[next_row][next_col] = char # .upper()

    board.print(board.start, direction)
    print(f"{expected_next_direction = } {next_direction = }")
    print()


def solution(filename: str, side_side: int, layout: List[str], stiches: Dict) -> int:
    board_map, raw_path_instructions = parse(filename, side_side, layout, stiches)
    path_instructions: List = parse_instructions(raw_path_instructions)

    for face, directions in stiches.items():
        for direction in directions:
            test_stich_rule(
                board_map, face, stiches[face][direction], direction, side_side
            )
            board_map.regen()

    # test_stich_rule(board_map, "w", stiches["w"][Direction.up], Direction.up, side_side)
    # test_stich_rule(board_map, "w", stiches["w"][Direction.left], Direction.left, side_side)
    # test_stich_rule(board_map, "g", stiches["g"][Direction.left], Direction.left, side_side)

    # face = "g"
    # direction = Direction.down
    # test_stich_rule(board_map, face, stiches[face][direction], direction, side_side)

    # face = "g"
    # direction = Direction.right
    # test_stich_rule(board_map, face, stiches[face][direction], direction, side_side)

    # face = "r"
    # direction = Direction.up
    # test_stich_rule(board_map, face, stiches[face][direction], direction, side_side)

    # face = "r"
    # direction = Direction.left
    # test_stich_rule(board_map, face, stiches[face][direction], direction, side_side)

    # face = "o"
    # direction = Direction.up
    # test_stich_rule(board_map, face, stiches[face][direction], direction, side_side)

    # face = "o"
    # direction = Direction.down
    # test_stich_rule(board_map, face, stiches[face][direction], direction, side_side)

    # face = "o"
    # direction = Direction.right
    # test_stich_rule(board_map, face, stiches[face][direction], direction, side_side)

    # face = "b"
    # direction = Direction.left
    # test_stich_rule(board_map, face, stiches[face][direction], direction, side_side)

    # face = "b"
    # direction = Direction.right
    # test_stich_rule(board_map, face, stiches[face][direction], direction, side_side)

    # face = "y"
    # direction = Direction.down
    # test_stich_rule(board_map, face, stiches[face][direction], direction, side_side)

    # face = "y"
    # direction = Direction.right
    # test_stich_rule(board_map, face, stiches[face][direction], direction, side_side)


if __name__ == "__main__":
    example_layout = [
        "  w",
        "grb",
        "  yo",
    ]
    fs: int = 3  # face side - 1

    example_stitches = {
        "b": {Direction.right: ("o", Direction.down, (0, 0, 0), (1, 0, -fs))},  # f((c, r), (c, r)) ??
        "y": {Direction.down: ("g", Direction.up, (0, 0, fs), (0, -1, fs))},   #row -> fs, invert cols
        "r": { Direction.up: ("w", Direction.left, (0, 1, 0), (0, 0, 0))},   #col -> row, col -> 0
    }

    # print(solution2("./example.txt", 4, example_layout, example_stitches))   # it should be 5031

    input_layout = [
        " wo",
        " b",
        "ry",
        "g",
    ]
    # TODO use diagram on notebook
    fs = 49
    stitches = {
        "w": {
            Direction.up: ("g", Direction.right, (0, 1, 0), (0, 0, 0)),  #
            Direction.left: ("r", Direction.right, (-1, 0, fs), (0, 0, 0)),  #
        },
        "g": {
            Direction.left: ("w", Direction.down, (0, 0, 0), (1, 0, 0)),  #
            Direction.down: ("o", Direction.down, (0, 0, 0), (0, 1, 0)),  #
            Direction.right: ("y", Direction.up, (0, 0, fs), (1, 0, 0)),  #
        },
        "r": {
            Direction.up: ("b", Direction.right, (0, 1, 0), (0, 0, 0)),  #
            Direction.left: ("w", Direction.right, (-1, 0, fs), (0, 0, 0)),  #
        },
        "o": {
            Direction.up: ("g", Direction.up, (0, 0, fs), (0, 1, 0)),  #
            Direction.down: ("b", Direction.left, (0, 1, 0), (0, 0, fs)),  #
            Direction.right: ("y", Direction.left, (-1, 0, fs), (0, 0, fs)),  #
        },
        "b": {
            Direction.left: ("r", Direction.down, (0, 0, 0), (1, 0, 0)),  #
            Direction.right: ("o", Direction.up, (0, 0, fs), (1, 0, 0)),  #
        },
        "y": {
            Direction.down: ("g", Direction.left, (0, 1, 0), (0, 0, fs)),  #
            Direction.right: ("o", Direction.left, (-1, 0, fs), (0, 0, fs)),  #
        },
    }
    print(
        solution2("./input.txt", 50, input_layout, stitches)
    ) 
