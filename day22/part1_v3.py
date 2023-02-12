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
    def __init__(self, board_map: List[str]) -> None:

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

        # connect nodes
        for row_number, row in enumerate(node_board):
            for col_number, node in enumerate(row):
                if node is None:
                    continue

                # right connection
                next_col: int = (col_number + 1) % self.ncols
                while node_board[row_number][next_col] == None:
                    next_col = (next_col + 1) % self.ncols
                node.right = node_board[row_number][next_col]

                # left connection
                prev_col: int = (col_number - 1) % self.ncols
                while node_board[row_number][prev_col] == None:
                    prev_col = (prev_col - 1) % self.ncols
                node.left = node_board[row_number][prev_col]

                # up connection
                upper_row: int = (row_number - 1) % self.nrows
                while node_board[upper_row][col_number] == None:
                    upper_row = (upper_row - 1) % self.nrows
                node.up = node_board[upper_row][col_number]

                # down connection
                down_row: int = (row_number + 1) % self.nrows
                while node_board[down_row][col_number] == None:
                    down_row = (down_row + 1) % self.nrows
                node.down = node_board[down_row][col_number]

                node.pointers: Dict[Direction, BoardNode] = {
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


def parse(filename: str) -> Tuple[List[str], str]:
    with open(filename, "r") as fp:
        data: str = fp.read()

    str_board_map, str_path_instructions = data.split("\n\n")
    board_map: List[str] = str_board_map.splitlines()
    path_instructions: List[str] = str_path_instructions[:-1]

    return Board(board_map), path_instructions


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

    return (
        1_000 * (current_position.row + 1)
        + 4 * (current_position.col + 1)
        + direction_value[facing]
    )


def solution(filename: str):
    board_map, raw_path_instructions = parse(filename)
    path_instructions: List = parse_instructions(raw_path_instructions)
    # board_map.print()
    # return 0
    return solve(board_map, path_instructions)


if __name__ == "__main__":
    print(solution("./example.txt"))
    print(solution("./input.txt"))
