import math
from typing import List


ROCK = "#"
AIR = "."
SAND = "+"
REST = "o"


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    max_x: int = 0
    max_y: int = 0
    min_x: int = float("inf")

    scan: List = []
    for line in data:
        path: List = []
        for pair in line.split(" -> "):
            coords = [int(coord) for coord in pair.split(",")]
            max_x = max(max_x, coords[0])
            max_y = max(max_y, coords[1])
            min_x = min(min_x, coords[0])
            path.append(coords)
        scan.append(path)

    max_y += 2
    min_x = min(min_x, 500 - max_y - 1)
    max_x = max(max_x, 500 + max_y + 1)

    drawing_rows = max_y + 1  # sand needs to float from 0
    drawing_cols = max_x - min_x + 1

    drawing: List[List[str]] = [[AIR] * drawing_cols for _ in range(drawing_rows)]

    # draw map from scan
    for path in scan:
        for index in range(1, len(path)):
            origin_x, origin_y = path[index - 1]
            destination_x, destination_y = path[index]

            x_direction: int = int(math.copysign(1, destination_x - origin_x))
            y_direction: int = int(math.copysign(1, destination_y - origin_y))
            for x in range(origin_x, destination_x + x_direction, x_direction):
                for y in range(origin_y, destination_y + y_direction, y_direction):
                    drawing[y][x - min_x] = ROCK

    # add floor
    for col_index in range(drawing_cols):
        drawing[-1][col_index] = ROCK

    rest_counter: int = 0
    steps = [
        (1, 0),  # down
        (1, -1),  # left-down
        (1, 1),  # right-down
    ]
    while True:
        # drop sand
        sand = [0, 500 - min_x]
        drawing[sand[0]][sand[1]] = SAND

        # sand fall
        while True:
            if (
                # down will fall forever
                sand[0] + 1 >= drawing_rows
                # left-down will fall forever
                or (
                    sand[0] + 1 >= drawing_rows
                    or sand[1] - 1 < 0
                    or sand[1] - 1 >= drawing_cols
                )
                # right-down will fall forever
                or (
                    sand[0] + 1 >= drawing_rows
                    or sand[1] + 1 < 0
                    or sand[1] + 1 >= drawing_cols
                )
            ):
                return rest_counter

            # try to move
            for step_row, step_col in steps:
                if drawing[sand[0] + step_row][sand[1] + step_col] == AIR:
                    drawing[sand[0]][sand[1]] = AIR
                    drawing[sand[0] + step_row][sand[1] + step_col] = SAND
                    sand = [sand[0] + step_row, sand[1] + step_col]
                    break
            else:
                drawing[sand[0]][sand[1]] = REST
                rest_counter += 1
                if sand == [0, 500 - min_x]:
                    return rest_counter
                break


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)

    result = solution("./input.txt")
    print(result)
