from collections import namedtuple
from typing import List, Set, Tuple

Point = namedtuple("Point", ["x", "y", "z"])


def parse(filename: str) -> List[Point]:
    with open(filename) as fp:
        data: List[str] = fp.read().splitlines()

    points: List[Point] = []
    for coord in data:
        coord_points: List[str] = coord.split(",")
        x: int = int(coord_points[0])
        y: int = int(coord_points[1])
        z: int = int(coord_points[2])
        points.append(Point(x, y, z))

    return points


def neighbors(point: Tuple[int, int, int]) -> List[Point]:
    x, y, z = point
    neighbors: List[Point] = [
        Point(x, y - 0.5, z),  # lower
        Point(x, y + 0.5, z),  # upper
        Point(x - 0.5, y, z),  # left
        Point(x + 0.5, y, z),  # right
        Point(x, y, z + 0.5),  # front
        Point(x, y, z - 0.5),  # back
    ]
    return neighbors


def solve(cubes: List[Point]) -> int:
    surfaces: Set[Point] = set()

    for cube in cubes:
        for neighbor in neighbors(cube):
            if neighbor in surfaces:
                surfaces.remove(neighbor)
            else:
                surfaces.add(neighbor)

    return len(surfaces)


def solution(filename: str) -> int:
    cubes: List[Point] = parse(filename)
    return solve(cubes)


if __name__ == "__main__":
    print(solution("./data/example1.txt"))  # 10
    print(solution("./data/example2.txt"))  # 64
    print(solution("./data/input.txt"))  # 3326
