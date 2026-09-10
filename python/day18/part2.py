from collections import deque, namedtuple
from typing import Deque, List, Set

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


def neighbor_surfaces(coord: Point) -> List[Point]:
    x, y, z = coord
    neighbors: List[Point] = [
        Point(x, y - 0.5, z),  # lower
        Point(x, y + 0.5, z),  # upper
        Point(x - 0.5, y, z),  # left
        Point(x + 0.5, y, z),  # right
        Point(x, y, z + 0.5),  # front
        Point(x, y, z - 0.5),  # back
    ]
    return neighbors


def neighbor_points(coord: Point) -> List[Point]:
    x, y, z = coord
    neighbors: List[Point] = [
        Point(x, y - 1, z),  # lower
        Point(x, y + 1, z),  # upper
        Point(x - 1, y, z),  # left
        Point(x + 1, y, z),  # right
        Point(x, y, z + 1),  # front
        Point(x, y, z - 1),  # back
    ]
    return neighbors


def solve(cubes: List[Point]) -> int:
    surfaces: Set[Point] = set()
    min_x: int = float("inf")  # type: ignore
    min_y: int = float("inf")  # type: ignore
    min_z: int = float("inf")  # type: ignore

    max_x: int = float("-inf")  # type: ignore
    max_y: int = float("-inf")  # type: ignore
    max_z: int = float("-inf")  # type: ignore

    for cube in cubes:
        x, y, z = cube

        min_x = min(min_x, x)
        min_y = min(min_y, y)
        min_z = min(min_z, z)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)

        for neighbor in neighbor_surfaces(cube):
            if neighbor in surfaces:
                surfaces.remove(neighbor)
            else:
                surfaces.add(neighbor)

    # adjust limits
    min_x -= 1
    min_y -= 1
    min_z -= 1
    max_x += 1
    max_y += 1
    max_z += 1

    # BFS setup
    start: Point = Point(min_x, min_y, min_z)
    queue: Deque[Point] = deque([start])
    visited: Set[Point] = set([start])

    air: Set[Point] = set()

    # BFS
    while queue:
        x, y, z = coord = queue.popleft()

        if coord in cubes:
            continue

        air.add(coord)

        for neighbor in neighbor_points(coord):
            new_x, new_y, new_z = neighbor
            if (
                min_x <= new_x <= max_x
                and min_y <= new_y <= max_y
                and min_z <= new_z <= max_z
            ):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)

    external_surface: Set[Point] = set()
    for cube in air:
        for neighbor in neighbor_surfaces(cube):
            if neighbor in surfaces:
                external_surface.add(neighbor)

    return len(external_surface)


def solution(filename: str) -> int:
    cubes: List[Point] = parse(filename)
    return solve(cubes)


if __name__ == "__main__":
    print(solution("./data/example2.txt"))  # 58
    print(solution("./data/input.txt"))  # 1996
