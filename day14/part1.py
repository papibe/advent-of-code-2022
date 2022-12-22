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
    min_y: int = float("inf")

    scan: List = []
    for line in data:
        path: List = []
        for pair in line.split(" -> "):
            coords = [int(coord) for coord in pair.split(",")]
            max_x = max(max_x, coords[0])
            max_y = max(max_y, coords[1])
            min_x = min(min_x, coords[0])
            min_y = min(min_y, coords[1])
            path.append(coords)
        scan.append(path)

    # for path in scan:
    #     print(path)
    # print(f"{min_x = }, {max_x = }")
    # print(f"{min_y = }, {max_y = }")

    drawing_rows = max_y + 1  # sand needs to float from 0
    drawing_cols = max_x - min_x + 1

    # print(f"{drawing_rows = }, {drawing_cols = }")

    drawing: List[List[str]] = [[AIR] * drawing_cols for _ in range(drawing_rows)]

    for path in scan:
        for index in range(1, len(path)):
            # print(path[index - 1], path[index])
            origin_x, origin_y = path[index - 1]
            destination_x, destination_y = path[index]
            # print(f"{origin_x = }, {origin_y = }\t{destination_x = }, {destination_y = }")

            x_direction: int = int(math.copysign(1, destination_x - origin_x))
            y_direction: int = int(math.copysign(1, destination_y - origin_y))
            for x in range(origin_x, destination_x + x_direction, x_direction):
                for y in range(origin_y, destination_y + y_direction, y_direction):
                    # print(f"{y = } {x = }\t{y}, {x - min_x}")
                    drawing[y][x - min_x] = ROCK

    # for line in drawing:
    #     print(''.join(line), len(line))

    sand_couter: int = 0
    rest_counter: int = 0
    while True:
        # drop sand
        sand = [0, 500 - min_x]
        drawing[sand[0]][sand[1]] = SAND

        # sand fall
        fall_counter: int = 0
        while True:
            # for line in drawing:
            #     print("".join(line), len(line))

            # try down
            new_sand: List[int] = None
            if sand[0] + 1 >= drawing_rows:
                return rest_counter

            if drawing[sand[0] + 1][sand[1]] == AIR:
                drawing[sand[0]][sand[1]] = AIR
                drawing[sand[0] + 1][sand[1]] = SAND
                sand = [sand[0] + 1, sand[1]]
                continue

            # try left down
            if sand[0] + 1 >= drawing_rows or sand[1] - 1 < 0  or sand[1] - 1 >= drawing_cols:
                return rest_counter

            if drawing[sand[0] + 1][sand[1] - 1] == AIR:
                drawing[sand[0]][sand[1]] = AIR
                drawing[sand[0] + 1][sand[1] - 1] = SAND
                sand = [sand[0] + 1, sand[1] - 1]
                continue

            # try right down
            if sand[0] + 1 >= drawing_rows or sand[1] + 1 < 0 or sand[1] + 1 >= drawing_cols:
                return rest_counter

            if drawing[sand[0] + 1][sand[1] + 1] == AIR:
                drawing[sand[0]][sand[1]] = AIR
                drawing[sand[0] + 1][sand[1] + 1] = SAND
                sand = [sand[0] + 1, sand[1] + 1]
                continue

            drawing[sand[0]][sand[1]] = REST
            rest_counter += 1
            break


            # for line in drawing:
            #     print("".join(line), len(line))
            # print(f"{rest_counter = }")

            # fall_counter += 1
            # if fall_counter == 25:
            #     break

        # sand_couter += 1
        # if sand_couter == 25:
        #     break
    return 0


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)

    result = solution("./input.txt")
    print(result)
