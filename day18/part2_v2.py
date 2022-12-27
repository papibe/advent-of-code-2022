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
    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = float("-inf")

    for cube in cubes:
        x, y, z = cube
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        min_z = min(min_z, z)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)

        for neighbor in neighbors(cube):
            if neighbor in surfaces:
                surfaces.remove(neighbor)
            else:
                surfaces.add(neighbor)

    internal_surfaces: Set = set()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                if (x, y, z) not in cubes:
                    # print(x, y, z)
                    outer_surfaces: Set = set()
                    left_min = (
                        right_min
                    ) = top_min = bottom_min = front_min = back_min = float("inf")
                    for sx, sy, sz in surfaces:
                        # x plane
                        if y == sy and z == sz and sx > x:
                            outer_surfaces.add("left")
                            if abs(sx - x) < left_min:
                                min_left_surface = (sx, sy, sz)
                                left_min = abs(sx - x)

                        if y == sy and z == sz and sx < x:
                            outer_surfaces.add("right")
                            if abs(sx - x) < right_min:
                                min_right_surface = (sx, sy, sz)
                                right_min = abs(sx - x)

                        # y plane
                        if x == sx and z == sz and sy > y:
                            outer_surfaces.add("top")
                            if abs(sy - y) < top_min:
                                min_top_surface = (sx, sy, sz)
                                top_min = abs(sy - y)

                        if x == sx and z == sz and sy < y:
                            outer_surfaces.add("bottom")
                            if abs(sy - y) < bottom_min:
                                min_bottom_surface = (sx, sy, sz)
                                bottom_min = abs(sy - y)

                        # z plane
                        if x == sx and y == sy and sz > z:
                            outer_surfaces.add("front")
                            if abs(sz - z) < front_min:
                                min_front_surface = (sx, sy, sz)
                                front_min = abs(sz - z)

                        if x == sx and y == sy and sz < z:
                            outer_surfaces.add("back")
                            if abs(sz - z) < back_min:
                                min_back_surface = (sx, sy, sz)
                                back_min = abs(sz - z)

                    if len(outer_surfaces) == 6:
                        internal_surfaces.add(min_left_surface)
                        internal_surfaces.add(min_right_surface)
                        internal_surfaces.add(min_top_surface)
                        internal_surfaces.add(min_bottom_surface)
                        internal_surfaces.add(min_front_surface)
                        internal_surfaces.add(min_back_surface)

    return len(surfaces) - len(internal_surfaces)


def solution(filename: str) -> int:
    cubes: List[Tuple[int, int, int]] = parse(filename)
    return solve(cubes)


if __name__ == "__main__":
    result: int = solution("./example1.txt")
    print(result)  # it should be 10

    result = solution("./example2.txt")
    print(result)  # it should be 58

    result = solution("./example3.txt")
    print(result)  # it should be 30

    result = solution("./input.txt")
    print(result)
