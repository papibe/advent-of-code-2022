from collections import deque, namedtuple
from typing import Deque, List, Set, Tuple

START: str = "S"
END: str = "E"

type Grid = List[List[str]]
Position = namedtuple("Position", ["row", "col"])


def parse(filename: str) -> Tuple[Grid, Position, Position]:
    with open(filename, "r") as fp:
        raw_data: str = fp.read()

    grid: Grid = []
    for line in raw_data.splitlines():
        grid.append([char for char in line])

    # find start and end
    start: Position
    end: Position
    for i, row in enumerate(grid):
        for j, elevation in enumerate(row):
            if elevation == START:
                start = Position(i, j)
            elif elevation == END:
                end = Position(i, j)

    # patch start and end points
    grid[start.row][start.col] = "a"
    grid[end.row][end.col] = "z"

    return grid, start, end


def is_at_most_one_higher(neighbor: Position, current: Position, grid: Grid) -> bool:
    neighbor_char: str = grid[neighbor.row][neighbor.col]
    current_char: str = grid[current.row][current.col]

    return (ord(neighbor_char) - ord(current_char)) <= 1


def neighbors(position: Position, max_row: int, max_col: int) -> List[Position]:
    steps: List[Tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    result: List[Position] = []
    for step_row, step_col in steps:
        if (
            0 <= position.row + step_row < max_row
            and 0 <= position.col + step_col < max_col
        ):
            result.append(Position(position.row + step_row, position.col + step_col))
    return result


def solve(grid: Grid, start: Position, end: Position) -> int:
    # BFS for shortest path

    # BFS initialization
    max_rows: int = len(grid)
    max_cols: int = len(grid[0])
    queue: Deque[Tuple[Position, int]] = deque([(start, 0)])
    visited: Set[Position] = {start}

    # main BFS traverse
    while queue:
        current, steps = queue.popleft()
        if current == end:
            return steps

        for neighbor in neighbors(current, max_rows, max_cols):
            if neighbor not in visited and is_at_most_one_higher(
                neighbor, current, grid
            ):
                queue.append((neighbor, steps + 1))
                visited.add(neighbor)

    return -1


def solution(filename: str) -> int:
    grid, start, end = parse(filename)
    return solve(grid, start, end)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 31
    print(solution("./input.txt"))  # 425
