import math
from typing import List, Tuple

ROCK = "#"
AIR = "."
SAND = "+"
REST = "o"

type Cave = List[List[str]]


def parse(filename: str) -> Tuple[Cave, int, int]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    max_x: int = 0
    max_y: int = 0
    min_x: int = float("inf")  # type: ignore
    min_y: int = float("inf")  # type: ignore

    scan: List[List[List[int]]] = []
    for line in data:
        path: List[List[int]] = []
        for pair in line.split(" -> "):
            coords = [int(coord) for coord in pair.split(",")]
            max_x = max(max_x, coords[0])
            max_y = max(max_y, coords[1])
            min_x = min(min_x, coords[0])
            min_y = min(min_y, coords[1])
            path.append(coords)
        scan.append(path)

    drawing_rows = max_y + 1  # sand needs to float from 0
    drawing_cols = max_x - min_x + 1

    drawing: List[List[str]] = [[AIR] * drawing_cols for _ in range(drawing_rows)]

    for path in scan:
        for index in range(1, len(path)):
            origin_x, origin_y = path[index - 1]
            destination_x, destination_y = path[index]

            x_direction: int = int(math.copysign(1, destination_x - origin_x))
            y_direction: int = int(math.copysign(1, destination_y - origin_y))
            for x in range(origin_x, destination_x + x_direction, x_direction):
                for y in range(origin_y, destination_y + y_direction, y_direction):
                    drawing[y][x - min_x] = ROCK

    return drawing, 0, 500 - min_x


def solve(drawing: Cave, sand_start_row: int, sand_start_col: int) -> int:

    drawing_rows: int = len(drawing)
    drawing_cols: int = len(drawing[0])

    mins: List[int] = [float("inf")] * drawing_cols  # type: ignore

    for col in range(drawing_cols):
        for row in range(drawing_rows):
            if drawing[row][col] == ROCK:
                mins[col] = min(mins[col], row)

    rest_counter: int = 0
    while True:
        # drop sand
        sand_row: int = sand_start_row
        sand_col: int = sand_start_col
        drawing[sand_row][sand_col] = SAND

        while True:
            # try down
            if sand_row + 1 >= drawing_rows:
                return rest_counter

            if drawing[sand_row + 1][sand_col] == AIR:
                new_sand_row = max(sand_row + 1, mins[sand_col] - 1)
                drawing[sand_row][sand_col] = AIR
                drawing[new_sand_row][sand_col] = SAND
                sand_row = new_sand_row
                continue

            # try left down
            if (
                sand_row + 1 >= drawing_rows
                or sand_col - 1 < 0
                or sand_col - 1 >= drawing_cols
            ):
                return rest_counter

            if drawing[sand_row + 1][sand_col - 1] == AIR:
                drawing[sand_row][sand_col] = AIR
                drawing[sand_row + 1][sand_col - 1] = SAND
                sand_row += 1
                sand_col -= 1

                continue

            # try right down
            if (
                sand_row + 1 >= drawing_rows
                or sand_col + 1 < 0
                or sand_col + 1 >= drawing_cols
            ):
                return rest_counter

            if drawing[sand_row + 1][sand_col + 1] == AIR:
                drawing[sand_row][sand_col] = AIR
                drawing[sand_row + 1][sand_col + 1] = SAND
                sand_row += 1
                sand_col += 1
                continue

            drawing[sand_row][sand_col] = REST
            mins[sand_col] = min(mins[sand_col], sand_row)
            rest_counter += 1
            break

    return -1


def solution(filename: str) -> int:
    drawing, sand_row, sand_col = parse(filename)
    return solve(drawing, sand_row, sand_col)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 24
    print(solution("./input.txt"))  # 897
