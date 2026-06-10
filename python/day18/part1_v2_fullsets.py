from typing import List, Tuple, Dict, Set

from part1 import parse


def neighbors(coord: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    x, y, z = coord
    neighbors: List = [
        (x, y, z, x + 1, y, z + 1),  # lower
        (x, y + 1, z, x + 1, y + 1, z + 1),  # upper
        (x, y, z, x, y + 1, z + 1),  # left
        (x + 1, y, z, x + 1, y + 1, z + 1),  # right
        (x, y, z + 1, x + 1, y + 1, z + 1),  # front
        (x, y, z, x + 1, y + 1, z),  # back
    ]
    return set(neighbors)


def solve(cubes: List[Tuple[int, int, int]]) -> int:
    surfaces: Set = set()
    for cube in cubes:
        surfaces = surfaces.symmetric_difference(neighbors(cube))

    return len(surfaces)


def solution(filename: str) -> int:
    cubes: List[Tuple[int, int, int]] = parse(filename)
    return solve(cubes)


if __name__ == "__main__":
    result: int = solution("./data/example1.txt")
    print(result)  # it should be 10

    result = solution("./data/example2.txt")
    print(result)  # it should be 64

    result = solution("./data/input.txt")
    print(result)
