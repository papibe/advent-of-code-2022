from collections import namedtuple
from typing import List, Set

ROCK = "#"
AIR = "."
SAND = "+"
REST = "o"

Coord = namedtuple("Coord", ["x", "y"])


class Cave:
    def __init__(
        self,
        grid: Set[Coord],
        max_x: int,
        max_y: int,
        min_x: int,
        min_y: int,
    ) -> None:
        self.grid: Set[Coord] = grid
        self.max_x: int = max_x
        self.max_y: int = max_y
        self.min_x: int = min_x
        self.min_y: int = min_y

        self.full: bool = False

        mins = {x: float("inf") for x in range(min_x, max_x + 1)}
        for x, y in grid:
            mins[x] = min(mins[x], y)
        self.mins = mins

    def is_full(self) -> bool:
        return self.full

    def main_drop_sand(self, sand: Coord) -> None:
        self.sand = sand

    def stable_sand(self) -> bool:
        # down: Coord = Coord(self.sand.x, self.sand.y + 1)
        if (self.sand.x, self.sand.y + 1) not in self.grid:
            return False

        # left_down: Coord = Coord(self.sand.x - 1, self.sand.y + 1)
        if (self.sand.x - 1, self.sand.y + 1) not in self.grid:
            return False

        # right_down: Coord = Coord(self.sand.x + 1, self.sand.y + 1)
        if (self.sand.x + 1, self.sand.y + 1) not in self.grid:
            return False

        self.grid.add(self.sand)
        self.mins[self.sand.x] = min(self.mins[self.sand.x], self.sand.y)

        return True

    def drop_sand(self) -> None:
        # try down
        if (self.sand.x, self.sand.y + 1) not in self.grid:
            self.sand = Coord(
                self.sand.x, max(self.sand.y + 1, self.mins[self.sand.x] - 1)
            )

        # try left down
        elif (self.sand.x - 1, self.sand.y + 1) not in self.grid:
            self.sand = Coord(self.sand.x - 1, self.sand.y + 1)

        # try right down
        elif (self.sand.x + 1, self.sand.y + 1) not in self.grid:
            self.sand = Coord(self.sand.x + 1, self.sand.y + 1)

        if (
            self.sand.y > self.max_y
            or self.sand.x > self.max_x
            or self.sand.x < self.min_x
        ):
            self.full = True


def parse(filename: str) -> Cave:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    max_x: int = 0
    max_y: int = 0
    min_x: int = float("inf")  # type: ignore
    min_y: int = float("inf")  # type: ignore

    paths: Set[Coord] = set()
    for line in data:
        path: List[Coord] = []
        for pair in line.split(" -> "):
            split_coords = pair.split(",")
            coords = Coord(int(split_coords[0]), int(split_coords[1]))

            max_x = max(max_x, coords.x)
            max_y = max(max_y, coords.y)
            min_x = min(min_x, coords.x)
            min_y = min(min_y, coords.y)

            path.append(coords)

        for i in range(len(path) - 1):
            start: Coord = path[i]
            end: Coord = path[i + 1]
            paths.add(start)
            paths.add(end)

            path_min_x = min(start.x, end.x)
            path_max_x = max(start.x, end.x)

            path_min_y = min(start.y, end.y)
            path_max_y = max(start.y, end.y)

            for x in range(path_min_x, path_max_x + 1):
                for y in range(path_min_y, path_max_y + 1):
                    paths.add(Coord(x, y))

    return Cave(paths, max_x, max_y, min_x, min_y)


def solve(cave: Cave) -> int:
    resting_sand: int = 0

    while not cave.is_full():
        # drop sand
        cave.main_drop_sand(Coord(500, 0))
        while not cave.stable_sand() and not cave.is_full():
            cave.drop_sand()

        if not cave.is_full():
            resting_sand += 1

    return resting_sand


def solution(filename: str) -> int:
    cave: Cave = parse(filename)
    return solve(cave)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 24
    print(solution("./input.txt"))  # 897
