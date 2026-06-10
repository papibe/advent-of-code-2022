from collections import deque
from typing import List, Tuple, Dict, Set, Union, Deque

Point = Tuple[int, int, int]


def parse(filename: str) -> List[Point]:
    with open(filename) as fp:
        data: List[str] = fp.read().splitlines()

    return [tuple(map(int, coords.split(","))) for coords in data]


def neighbors(coord: Point) -> List[Point]:
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


def sneighbors(coord: Point) -> List[Point]:
    x, y, z = coord
    neighbors: List = [
        (x, y - 1, z),  # lower
        (x, y + 1, z),  # upper
        (x - 1, y, z),  # left
        (x + 1, y, z),  # right
        (x, y, z + 1),  # front
        (x, y, z - 1),  # back
    ]
    return neighbors


def is_external(
    surface: Point, surfaces: List[Point], min_point: Point, max_point: Point
) -> bool:
    # queue: Deque = deque([surface])
    queue: Deque = deque()
    queue.append(surface)
    visited: Set = {surface}

    # print(queue, visited)

    while queue:
        face: Point = queue.popleft()

        if face in surfaces:
            # print(face, "on surfaces")
            continue

        if (
            face[0] < min_point[0]
            or face[1] < min_point[1]
            or face[2] < min_point[2]
            or face[0] > max_point[0]
            or face[1] > max_point[1]
            or face[2] > max_point[2]
        ):
            # print(face, "is out")
            return True

        for neighbor in sneighbors(face):
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

    # print(surface, "is internal")
    return False


def solve(cubes: List[Point]) -> int:
    surfaces: Set = set()
    min_point = [float("inf"), float("inf"), float("inf")]
    max_point = [float("-inf"), float("-inf"), float("-inf")]

    for cube in cubes:
        x, y, z = cube

        min_point = [min(min_point[0], x), min(min_point[1], y), min(min_point[2], z)]
        max_point = [max(max_point[0], x), max(max_point[1], y), max(max_point[2], z)]

        for neighbor in neighbors(cube):
            if neighbor in surfaces:
                surfaces.remove(neighbor)
            else:
                surfaces.add(neighbor)

    # print(min_point, max_point)

    internal_surfaces: Set = set()
    for surface in surfaces:
        for neighbor in sneighbors(surface):
            if is_external(neighbor, surfaces, min_point, max_point):
                break
        else:
            internal_surfaces.add(surface)

    print(len(surfaces), len(internal_surfaces))

    return len(surfaces) - len(internal_surfaces)


def solution(filename: str) -> int:
    cubes: List[Point] = parse(filename)
    return solve(cubes)


if __name__ == "__main__":
    result: int = solution("./data/example1.txt")
    print(result)  # it should be 10

    result = solution("./data/example2.txt")
    print(result)  # it should be 58

    result = solution("./data/example3.txt")
    print(result)  # it should be 30

    result = solution("./data/input.txt")
    print(result)
