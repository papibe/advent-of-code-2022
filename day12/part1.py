from typing import List, Set, Tuple, Deque
from collections import deque

START = "S"
END = "E"


def is_at_most_one_higher(neighbor: Tuple, current: Tuple, grid) -> bool:
    n_row, n_col = neighbor
    c_row, c_col = current
    neighbor_char: str = grid[n_row][n_col]
    current_char: str = grid[c_row][c_col]

    return (ord(neighbor_char) - ord(current_char)) <= 1


def neighbors(
    position: Tuple[int, int], max_row: int, max_col: int
) -> List[Tuple[int, int]]:

    current_row, current_col = position
    steps = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    result: List[Tuple[int, int]] = []
    for step_row, step_col in steps:
        if (
            0 <= current_row + step_row < max_row
            and 0 <= current_col + step_col < max_col
        ):
            result.append((current_row + step_row, current_col + step_col))
    return result


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        raw_data: str = fp.read()

    grid: List[List[str]] = []
    for line in raw_data.splitlines():
        grid.append([char for char in line])

    # for row in grid:
    #     for item in row:
    #         print(item, end="")
    #     print()

    for i, row in enumerate(grid):
        for j, elevation in enumerate(row):
            if elevation == START:
                start: tuple[str, str] = (i, j)
            elif elevation == END:
                end: tuple[str, str] = (i, j)
        #         break
        # else:
        #     continue
        # break

    print(start)
    print(end)

    # patch start point
    grid[start[0]][start[1]] = "a"
    grid[end[0]][end[1]] = "z"

    # BFS for shortest path

    # initialization
    max_rows: int = len(grid)
    max_cols: int = len(grid[0])
    queue: Deque = deque()
    queue.append((start, []))
    print(queue)
    visited: Set[Tuple[int, int]] = {start}

    # main traverse
    while queue:
        current, path = queue.popleft()
        # print(f"{current = }, {path = }")
        if current == end:
            print("We arrived")
            final_path = path
            break
        for neighbor in neighbors(current, max_rows, max_cols):
            if neighbor not in visited and is_at_most_one_higher(
                neighbor, current, grid
            ):
                new_path = path[:]
                new_path.append(neighbor)
                queue.append((neighbor, new_path))

                visited.add(neighbor)

    return len(final_path)


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 31

    result = solution("./input.txt")
    print(result)
