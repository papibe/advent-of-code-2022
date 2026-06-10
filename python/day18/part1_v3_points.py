from typing import List, Tuple, Dict, Set


def parse(filename: str) -> List[Tuple[int, int, int]]:
    with open(filename) as fp:
        data: List[str] = fp.read().splitlines()

    return [tuple(map(int, coords.split(","))) for coords in data]


def neighbors(coord: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    x, y, z = coord
    neighbors: List = [
        (x, y - 0.5, z),  # lower
        (x, y + 0.5, z),  # upper
        (x - 0.5, y, z),  # left
        (x + 0.5, y, z),  # right
        (x, y, z + 0.5),  # front
        (x, y, z - 0.5),  # back
    ]
    return neighbors


def solve(cubes: List[Tuple[int, int, int]]) -> int:
    surfaces: Set = set()

    for cube in cubes:
        for neighbor in neighbors(cube):
            if neighbor in surfaces:
                surfaces.remove(neighbor)
            else:
                surfaces.add(neighbor)

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
