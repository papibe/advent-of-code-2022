from typing import List, Dict, Tuple, Set


def print_grove(grove: Set) -> None:
    max_row: int = -1_000
    min_row: int = 1_000
    max_col: int = -1_000
    min_col: int = 1_000
    for (row, col) in grove:
        max_row = max(max_row, row)
        min_row = min(min_row, row)
        max_col = max(max_col, col)
        min_col = min(min_col, col)

    print(min_row, max_row, min_col, max_col)

    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            if (i, j) in grove:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def parse(filename: str) -> Set:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    grove: Set[Tuple[int, int]] = set()
    for row_number, line in enumerate(data):
        for col_number, item in enumerate(line):
            if item == "#":
                grove.add((row_number, col_number))

    print(grove)
    print_grove(grove)

    return grove


def rounds(grove: Set, nrounds: int) -> Set:
    for index in range(nrounds):
        grove = round(grove, index)
        print(grove)
    return grove


def all_neighbors(coord: Tuple[int, int]) -> List:
    row, col = coord
    return [
        (row + step_row, col + step_col)
        for step_row, step_col in [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
        ]
    ]


def north_lookup(coord: Tuple[int, int]) -> List:
    row, col = coord
    return [
        (row + step_row, col + step_col)
        for step_row, step_col in [(-1, -1), (-1, 0), (-1, 1)]
    ]


def south_lookup(coord: Tuple[int, int]) -> List:
    row, col = coord
    return [
        (row + step_row, col + step_col)
        for step_row, step_col in [(1, -1), (1, 0), (1, 1)]
    ]


def west_lookup(coord: Tuple[int, int]) -> List:
    row, col = coord
    return [
        (row + step_row, col + step_col)
        for step_row, step_col in [(1, -1), (0, -1), (-1, -1)]
    ]


def east_lookup(coord: Tuple[int, int]) -> List:
    row, col = coord
    return [
        (row + step_row, col + step_col)
        for step_row, step_col in [(1, 1), (0, 1), (-1, 1)]
    ]

def lookup_generator(index: int):
    functions = (
        (north_lookup, south_lookup, west_lookup, east_lookup),
        (south_lookup, west_lookup, east_lookup, north_lookup),
        (west_lookup, east_lookup, north_lookup, south_lookup),
        (east_lookup, north_lookup, south_lookup, west_lookup),
    )
    yield functions[index % 4]

def round(grove: Set[Tuple[int, int]], index: int) -> Set:
    count_moves: Dict = {}
    attempted_moves: Dict = {}

    for coord in grove:
        row, col = coord

        if all(nb not in grove for nb in all_neighbors(coord)):
            count_moves[coord] = count_moves.get(coord, 0) + 1
            attempted_moves[coord] = (row, col)
            print(row, col, "not moving")
            continue

        if all(nb not in grove for nb in north_lookup(coord)):
            north_coord = (row - 1, col)
            count_moves[north_coord] = count_moves.get(north_coord, 0) + 1
            attempted_moves[coord] = north_coord
            print(row, col, "moving north")
            continue

        if all(nb not in grove for nb in south_lookup(coord)):
            south_coord = (row + 1, col)
            count_moves[south_coord] = count_moves.get(south_coord, 0) + 1
            attempted_moves[coord] = south_coord
            print(row, col, "moving south")
            continue

        if all(nb not in grove for nb in west_lookup(coord)):
            west_coord = (row, col - 1) 
            count_moves[west_coord] = count_moves.get(west_coord, 0) + 1
            attempted_moves[coord] = west_coord
            print(row, col, "moving west")
            continue

        if all(nb not in grove for nb in east_lookup(coord)):
            east_coord = (row, col + 1)
            count_moves[east_coord] = count_moves.get(east_coord, 0) + 1
            attempted_moves[coord] = east_coord
            print(row, col, "moving east")
            continue

    print(f"{attempted_moves = }")
    print(f"{count_moves = }")

    next_grove: Set = set()
    for current, next_move in attempted_moves.items():
        if count_moves[next_move] == 1:
            next_grove.add(next_move)
        else:
            next_grove.add(current)

    print(next_grove)
    print_grove(next_grove)

    return next_grove


def count_ground(grove: Set) -> int:
    return 0


def solution(filename: str) -> int:
    grove: Set = parse(filename)
    final_grove: Set = rounds(grove, 10)
    return count_ground(final_grove)


if __name__ == "__main__":
    print(solution("./example1.txt"))
