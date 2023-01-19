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
    for _ in range(nrounds):
        grove = round(grove)
        print(grove)
    return grove


def round(grove: Set[Tuple[int, int]]) -> Set:
    not_moving: Set = set()
    attempted_moves: Dict = {}
    blocked_moves: Dict = {}

    for row, col in grove:
        if (
            (row - 1, col) not in grove
            and (row - 1, col + 1) not in grove
            and (row, col + 1) not in grove
            and (row + 1, col + 1) not in grove
            and (row + 1, col) not in grove
            and (row + 1, col - 1) not in grove
            and (row, col - 1) not in grove
        ):
            not_moving.add((row, col))
            print(row, col, "not moving")
            continue
        if (
            (row - 1, col) not in grove
            and (row - 1, col - 1) not in grove
            and (row - 1, col + 1) not in grove
        ):
            if (row - 1, col) in blocked_moves:
                continue
            if (row - 1, col) not in attempted_moves:
                attempted_moves[(row - 1, col)] = (row, col)
                print(row, col, "moving north")
            else:
                not_moving.add((row, col))
                del attempted_moves[(row - 1, col)]
                blocked_moves[(row - 1, col)] = True
            continue

        if (
            (row + 1, col) not in grove
            and (row + 1, col - 1) not in grove
            and (row + 1, col + 1) not in grove
        ):
            if (row + 1, col) in blocked_moves:
                continue
            if (row + 1, col) not in attempted_moves:
                attempted_moves[(row + 1, col)] = (row, col)
                print(row, col, "moving south")
            else:
                not_moving.add((row, col))
                del attempted_moves[(row + 1, col)]
                blocked_moves[(row + 1, col)] = True
            continue

        if (
            (row, col - 1) not in grove
            and (row - 1, col - 1) not in grove
            and (row + 1, col - 1) not in grove
        ):
            if (row, col - 1) in blocked_moves:
                continue
            if (row, col - 1) not in attempted_moves:
                attempted_moves[(row, col - 1)] = (row, col)
                print(row, col, "moving west")
            else:
                not_moving.add((row, col))
                del attempted_moves[(row, col - 1)]
                blocked_moves[(row, col - 1)] = True
            continue

        if (
            (row, col + 1) not in grove
            and (row - 1, col + 1) not in grove
            and (row + 1, col + 1) not in grove
        ):
            if (row, col + 1) in blocked_moves:
                continue
            if (row, col + 1) not in attempted_moves:
                attempted_moves[(row, col + 1)] = (row, col)
                print(row, col, "moving east")
            else:
                not_moving.add((row, col))
                del attempted_moves[(row, col + 1)]
                blocked_moves[(row, col + 1)] = True
            continue

    if not attempted_moves:
        return grove

    print(f"{not_moving = }")
    print(f"{attempted_moves = }")

    new_grove: Set = set()
    for k, v in attempted_moves.items():
        # print(f"{k = }, {v = }")
        if k not in not_moving and k not in blocked_moves:
            new_grove.add(k)
        else:
            new_grove.add(v)

    next_grove = not_moving | new_grove

    print(f"{next_grove =}")
    print_grove(new_grove)
    return next_grove


def count_ground(grove: Set) -> int:
    return 0


def solution(filename: str) -> int:
    grove: Set = parse(filename)
    final_grove: Set = rounds(grove, 10)
    return count_ground(final_grove)


if __name__ == "__main__":
    print(solution("./example1.txt"))
