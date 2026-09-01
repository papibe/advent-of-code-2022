import itertools
from enum import Enum
from typing import Callable, Dict, Iterator, List, Set, Tuple

_ROCKS = (
    (("@", "@", "@", "@"),),
    (
        (".", "@", "."),
        ("@", "@", "@"),
        (".", "@", "."),
    ),
    (
        ("@", "@", "@"),
        (".", ".", "@"),
        (".", ".", "@"),
    ),
    (
        ("@"),
        ("@"),
        ("@"),
        ("@"),
    ),
    (
        ("@", "@"),
        ("@", "@"),
    ),
)

ROCKS: List[List[Tuple[int, int]]] = []

for rock in _ROCKS:
    rock_coordinates: List[Tuple[int, int]] = []
    for i, row in enumerate(rock):
        for j, value in enumerate(row):
            if value == "@":
                rock_coordinates.append((i, j))
    ROCKS.append(rock_coordinates)


class Wind(Enum):
    left = "<"
    right = ">"


def get_wind_from_str(s: str) -> Wind:
    match s:
        case "<":
            return Wind.left
        case ">":
            return Wind.right
        case _:
            raise RuntimeError("Unknown wind character")


class Chamber:
    def __init__(self, width: int) -> None:
        self.chamber: Set[Tuple[int, int]] = set()
        self.width: int = width
        self.size: int = 0
        self.size_with_rock: int = 0
        self.stable: bool = True
        self.rock: Set[Tuple[int, int]] = set()

    def add_falling_rock(self, rock: List[Tuple[int, int]]) -> None:
        self.rock_row: int = self.size + 4
        self.rock_col: int = 2
        self.size_with_rock = self.size + 4 + (4)

        for x, y in rock:
            self.rock.add((self.rock_row + x, self.rock_col + y))

        self.stable = False

    def _move_right(self) -> None:
        new_rock_position: Set[Tuple[int, int]] = set()
        for row, col in self.rock:
            if col + 1 >= self.width or (row, col + 1) in self.chamber:
                return
            new_rock_position.add((row, col + 1))

        self.rock = new_rock_position

    def _move_left(self) -> None:
        new_rock_position: Set[Tuple[int, int]] = set()
        for row, col in self.rock:
            if col - 1 < 0 or (row, col - 1) in self.chamber:
                return
            new_rock_position.add((row, col - 1))

        self.rock = new_rock_position

    def fall_down(self) -> None:
        new_rock_position: Set[Tuple[int, int]] = set()
        for row, col in self.rock:
            if row - 1 < 1 or (row - 1, col) in self.chamber:
                self.stabilize()
                return
            new_rock_position.add((row - 1, col))

        self.rock = new_rock_position

    def stabilize(self) -> None:
        max_row: int = float("-inf")  # type: ignore

        for row, col in self.rock:
            max_row = max(max_row, row)
            self.chamber.add((row, col))

        self.rock = set()
        self.size = max(max_row, self.size)
        self.size_with_rock = max_row
        self.stable = True

    def gas_push(self, wind: Wind) -> None:
        wind_mapping: Dict[Wind, Callable[[], None]] = {
            Wind.left: self._move_left,
            Wind.right: self._move_right,
        }
        wind_mapping[wind]()

    def is_stable(self) -> bool:
        return self.stable


def solve(wind_data: List[Wind], chamber: Chamber, number_of_rocks: int) -> int:
    gas: Iterator[Wind] = itertools.cycle(wind_data)
    rocks: Iterator[List[Tuple[int, int]]] = itertools.cycle(ROCKS)

    for _ in range(number_of_rocks):
        rock: List[Tuple[int, int]] = next(rocks)
        chamber.add_falling_rock(rock)

        while not chamber.is_stable():
            wind: Wind = next(gas)
            chamber.gas_push(wind)
            chamber.fall_down()

    return chamber.size


def parse(filename: str) -> List[Wind]:
    with open(filename, "r") as fp:
        raw_data: str = fp.read().strip()

    return [get_wind_from_str(char) for char in raw_data]


def solution(filename: str, number_of_rocks: int) -> int:
    wind_data: List[Wind] = parse(filename)
    chamber: Chamber = Chamber(7)

    return solve(wind_data, chamber, number_of_rocks)


if __name__ == "__main__":
    print(solution("./example.txt", 2022))  # 3068
    print(solution("./input.txt", 2022))  # 3163
