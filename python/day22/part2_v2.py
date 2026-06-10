from enum import Enum, auto
from typing import List, Tuple, Dict


class Direction(Enum):
    right: str = auto()
    left: str = auto()
    up: str = auto()
    down: str = auto()


class BoardNode:
    def __init__(self, content: str, row: int, col: int) -> None:
        self.content: str = content
        self.row: int = row
        self.col: int = col
        self.face: int = None

        self.right: "BoardNode" = None
        self.left: "BoardNode" = None
        self.up: "BoardNode" = None
        self.down: "BoardNode" = None

        self.pointers: Dict[Direction, BoardNode] = {
            Direction.right: self.right,
            Direction.left: self.left,
            Direction.up: self.up,
            Direction.down: self.down,
        }

    def __repr__(self) -> str:
        return f"({self.row}, {self.col}) {self.content}"


class Board:
    def __init__(self, board_map: List[str], side_side: int) -> None:

        # get the max length of the longer line
        self.ncols: int = max([len(row) for row in board_map])
        self.nrows: int = len(board_map)

        # pad shorter lines with spaces
        full_board = []
        for row in board_map:
            full_board.append(row + " " * (self.ncols - len(row)))

        # create board of BoarNodes (unconnected yet)
        node_board: List[List[BoardNode]] = []
        for row_number, row in enumerate(full_board):
            node_row: List[BoardNode] = []
            for col_number, item in enumerate(row):
                if item == " ":
                    node_row.append(None)
                else:
                    node_row.append(BoardNode(item, row_number, col_number))
            node_board.append(node_row)

        # connect nodes that is possible to connect directly from the map
        for row_number, row in enumerate(node_board):
            for col_number, node in enumerate(row):
                if node is None:
                    continue

                # right connection
                next_col: int = col_number + 1
                if (
                    0 <= next_col < self.ncols
                    and node_board[row_number][next_col] is not None
                ):
                    node.right = node_board[row_number][next_col]

                # left connection
                prev_col: int = col_number - 1
                if (
                    0 <= next_col < self.ncols
                    and node_board[row_number][prev_col] is not None
                ):
                    node.left = node_board[row_number][prev_col]

                # up connection
                upper_row: int = row_number - 1
                if (
                    0 <= upper_row < self.nrows
                    and node_board[upper_row][col_number] is not None
                ):
                    node.up = node_board[upper_row][col_number]

                # down connection
                down_row: int = row_number + 1
                if (
                    0 <= down_row < self.nrows
                    and node_board[down_row][col_number] is not None
                ):
                    node.down = node_board[down_row][col_number]

        # begin connect faces --------------------------------------------------

        # left 1 with up 3
        row1: int = 0
        col1: int = side_side * 2

        row3: int = side_side
        col3: int = side_side

        for index in range(side_side):
            node_board[row1 + index][col1].left = node_board[row3][col3 + index]
            node_board[row3][col3 + index].up = node_board[row1 + index][col1]

        # up 1 with reverse up 2
        row1: int = 0
        col1: int = side_side * 2

        row2: int = side_side
        col2: int = side_side - 1

        for index in range(side_side):
            node_board[row1][col1 + index].up = node_board[row2][col2 - index]
            node_board[row2][col2 - index].up = node_board[row1][col1 + index]

        # right 1 with 6 right
        row1: int = 0
        col1: int = side_side * 3 - 1

        row6: int = side_side * 2
        col6: int = side_side * 4 - 1

        for index in range(side_side):
            # print((row1 + index, col1), (row6, col6 + index))
            node_board[row1 + index][col1].right = node_board[row6 + index][col6]
            node_board[row6 + index][col6].right = node_board[row1 + index][col1]

        # 2 left with 6 down
        row2: int = side_side
        col2: int = 0

        row6: int = side_side * 3 - 1
        col6: int = side_side * 3

        for index in range(side_side):
            # print((row1 + index, col1), (row6, col6 + index))
            node_board[row2 + index][col2].left = node_board[row6][col6 + index]
            node_board[row6][col6 + index].down = node_board[row2 + index][col2]

        # 2 down with 5 down
        row2: int = side_side * 2 - 1
        col2: int = 0

        row5: int = side_side * 3 - 1
        col5: int = side_side * 2

        for index in range(side_side):
            # print((row1 + index, col1), (row6, col6 + index))
            node_board[row2][col2 + index].down = node_board[row6][col6 + index]
            node_board[row6][col6 + index].down = node_board[row2][col2 + index]

        # 3 down with reverse 5 left
        row3: int = side_side * 2 - 1
        col3: int = side_side

        row5: int = side_side * 2
        col5: int = side_side * 3 - 1

        for index in range(side_side):
            # print((row1 + index, col1), (row6, col6 + index))
            node_board[row3][col3 + index].down = node_board[row5 - index][col5]
            node_board[row5 - index][col5].left = node_board[row3][col3 + index]

        # 4 right with reverse 6 up
        row4: int = side_side
        col4: int = side_side * 3 - 1

        row6: int = side_side * 2
        col6: int = side_side * 4 - 1

        for index in range(side_side):
            print((row4 + index, col4), (row6, col6 - index))
            node_board[row4 + index][col4].right = node_board[row6][col6 - index]
            node_board[row6][col6 - index].up = node_board[row4 + index][col4]
        # end connect faces ----------------------------------------------------

        # update pointers dictionary
        for row in node_board:
            for node in row:
                if node is not None:
                    node.pointers = {
                        Direction.right: node.right,
                        Direction.left: node.left,
                        Direction.up: node.up,
                        Direction.down: node.down,
                    }

        # get startting node
        for col_number, item in enumerate(node_board[0]):
            if item is not None:
                break
        self.start_row: int = 0
        self.start_col: int = col_number
        self.start_node: BoardNode = node_board[self.start_row][self.start_col]

        # TODO: node_map is not in the class?
        self.map = full_board
        self.rows = len(full_board)

    def get_start_node(self) -> Tuple[int, int]:
        return self.start_node

    def get(self, row: int, col: int) -> str:
        return self.map[row][col]

    def move(self, current: BoardNode, direction: Direction) -> Tuple:
        next_node: BoardNode = current.pointers[direction]
        if next_node.content != "#":
            return next_node
        else:
            return current

    def print(self):
        for row in self.map:
            for char in row:
                if char == " ":
                    print("x", end="")
                else:
                    print(char, end="")
            print()

        print()


def parse(filename: str, side_side: int) -> Tuple[List[str], str]:
    with open(filename, "r") as fp:
        data: str = fp.read()

    str_board_map, str_path_instructions = data.split("\n\n")
    board_map: List[str] = str_board_map.splitlines()
    path_instructions: List[str] = str_path_instructions[:-1]

    return Board(board_map, side_side), path_instructions


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


def move(
    position: BoardNode, direction: str, board_map: List[str], steps: int
) -> Tuple[int, int]:
    for _ in range(steps):
        next_position = board_map.move(position, direction)
        print(f"->{position = }, {next_position}")
        if next_position == position:
            print(f"{position = }")
            return position
        position = next_position

    print(f"{position = }")
    return position


def solve(board_map: Board, path: str) -> int:
    facing: str = Direction.right
    current_position: Tuple[int, int] = board_map.get_start_node()
    # print(current_position)
    # print(board_map[current_position[0]][current_position[1]])

    counter: int = 0
    for instruction in path:
        if instruction in ["L", "R"]:
            facing = rotate(facing, instruction)
            print(f"new {facing = }")
            continue
        steps = int(instruction)
        print(f"{steps = }")
        current_position = move(current_position, facing, board_map, steps)

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

    print(
        f"{current_position.row = }, {current_position.col = }, {direction_value[facing] = }"
    )

    return (
        1_000 * (current_position.row + 1)
        + 4 * (current_position.col + 1)
        + direction_value[facing]
    )


def solution(filename: str, side_side: int):
    board_map, raw_path_instructions = parse(filename, side_side)
    path_instructions: List = parse_instructions(raw_path_instructions)
    # board_map.print()
    # return 0
    return solve(board_map, path_instructions)


if __name__ == "__main__":
    print(solution("./example.txt", 4))
    # print(solution("./input.txt", 50))

    # 001
    # 234
    # 0056

    map = [
        "00w",
        "grb",
        "00yo",
    ]
    fs: int = 3 # face side
    stitches = {
        "w": {
            "top": (
                "g", (1, 0), (-1, fs)
            ),
            "right": (
                "o", (-1, fs), (1, 0)
            ),
            "bottom": (
                "b", (1, -fs), (1, 0)
            ),
            "left": (
                "r", (), () #0,0 -> 0,0  fs,0 -> 0,fs
            ),
        },
        "b": {
            "top": (
                "g", (0, 1), (0, fs - 1), (0, 1), (0, -1)
            ),
            "right": (
                "o", (0, fs - 1), (fs - 1, fs - 1), (1, 0), (-1, 0)
            ),
            "bottom": (
                "b", (fs - 1, 0), (0, 0), (0, 1), (0, 1)
            ),
            "left": (
                "r", (0, 0), (0, 0), (1, 0), (0, 1)
            ),
        },
    }


# 012
# 03
# 45
# 6
