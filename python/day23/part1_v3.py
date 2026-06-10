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

def count_empty_ground(grove: Set) -> None:
    max_row: int = float("-inf")
    min_row: int = float("inf")
    max_col: int = float("-inf")
    min_col: int = float("inf")
    for (row, col) in grove:
        print(row, col)
        max_row = max(max_row, row)
        min_row = min(min_row, row)
        max_col = max(max_col, col)
        min_col = min(min_col, col)

    print(min_row, max_row, min_col, max_col, len(grove))

    return ((max_row - min_row + 1) * (max_col - min_col + 1)) - len(grove)


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
        (( -1, 0, north_lookup), ( 1, 0, south_lookup), ( 0, -1, west_lookup), ( 0, 1, east_lookup)),
        (( 1, 0, south_lookup), ( 0, -1, west_lookup), ( 0, 1, east_lookup), ( -1, 0, north_lookup)),
        (( 0, -1, west_lookup), ( 0, 1, east_lookup), ( -1, 0, north_lookup), ( 1, 0, south_lookup)),
        (( 0, 1, east_lookup), ( -1, 0, north_lookup), ( 1, 0, south_lookup), ( 0, -1, west_lookup)),
    )
    return functions[index % 4]

def round(grove: Set[Tuple[int, int]], index: int) -> Set:
    count_moves: Dict = {}
    attempted_moves: Dict = {}

    staying_in_place: Set = set()

    lookup_generator_values = lookup_generator(index)

    for coord in grove:
        row, col = coord
        print(coord)

        if all(nb not in grove for nb in all_neighbors(coord)):

            staying_in_place.add(coord)

            # count_moves[coord] = count_moves.get(coord, 0) + 1
            # attempted_moves[coord] = (row, col)
            print(row, col, "not moving")
            continue

        print("-" * 50)
        for step_row, step_col, func in lookup_generator_values:
            # print(step_row, step_col, func)
            if all(nb not in grove for nb in func(coord)):           
                next_coord = (row + step_row, col + step_col)
                count_moves[next_coord] = count_moves.get(next_coord, 0) + 1
                attempted_moves[coord] = next_coord
                print(coord, next_coord, "->", func)
                break
        else:
            staying_in_place.add(coord)


    print(f"{len(staying_in_place) =}, {staying_in_place}")
    print(f"{len(attempted_moves) =}, {attempted_moves = }")
    print(f"{len(count_moves) =}, {count_moves = }")

    next_grove: Set = set()
    for current, next_move in attempted_moves.items():
        if count_moves[next_move] == 1 and next_move not in staying_in_place:
            next_grove.add(next_move)
        else:
            next_grove.add(current)

    # print(next_grove)
    new_grove: Set = staying_in_place | next_grove

    print(f"{len(grove) = }, {len(new_grove) = }")
    print_grove(new_grove)

    return new_grove


# def count_ground(grove: Set) -> int:
#     return 0


def solution(filename: str) -> int:
    grove: Set = parse(filename)
    final_grove: Set = rounds(grove, 10)
    return count_empty_ground(final_grove)


if __name__ == "__main__":
    # print(solution("./example1.txt"))
    # print(solution("./example2.txt"))
    print(solution("./input.txt"))
