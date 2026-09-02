import itertools
from collections import deque
from enum import Enum
from typing import Callable, Deque, Dict, FrozenSet, Iterator, List, Set, Tuple

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

ROCKS: List[Tuple[int, List[Tuple[int, int]]]] = []

for index, rock in enumerate(_ROCKS):
    rock_coordinates: List[Tuple[int, int]] = []
    for i, row in enumerate(rock):
        for j, value in enumerate(row):
            if value == "@":
                rock_coordinates.append((i, j))
    ROCKS.append((index, rock_coordinates))


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

    def trim(self) -> FrozenSet[Tuple[int, int]]:
        upper_limit: int = self.size + 1
        start: Tuple[int, int] = (upper_limit, 0)
        queue: Deque[Tuple[int, int]] = deque([start])
        visited: Set[Tuple[int, int]] = {start}

        new_chamber: Set[Tuple[int, int]] = set()
        min_row: int = float("inf")  # type: ignore

        while queue:
            row, col = queue.popleft()
            if (row, col) in self.chamber:
                new_chamber.add((row, col))
                continue

            for d_row, d_col in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                if 0 < row + d_row <= upper_limit and 0 <= col + d_col < self.width:
                    if (row + d_row, col + d_col) not in visited:
                        queue.append((row + d_row, col + d_col))
                        visited.add((row + d_row, col + d_col))
                        min_row = min(min_row, row + d_row)

        self.chamber = new_chamber

        state: Set[Tuple[int, int]] = set()
        for row, col in new_chamber:
            state.add((row - min_row, col))

        return frozenset(state)

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


def solve(
    wind_data: List[Tuple[int, Wind]], chamber: Chamber, number_of_rocks: int
) -> int:

    seen_state: Dict[Tuple[int, int, FrozenSet[Tuple[int, int]]], Tuple[int, int]] = {}
    min_chamber_state_size: int = float("inf")  # type: ignore
    max_chamber_state_size: int = float("-inf")  # type: ignore

    gas: Iterator[Tuple[int, Wind]] = itertools.cycle(wind_data)
    rocks: Iterator[Tuple[int, List[Tuple[int, int]]]] = itertools.cycle(ROCKS)

    current_number_of_rocks: int = 0
    while current_number_of_rocks < number_of_rocks:
        rock_index, rock = next(rocks)
        chamber.add_falling_rock(rock)

        while not chamber.is_stable():
            wind_index, wind = next(gas)
            chamber.gas_push(wind)
            chamber.fall_down()

        chamber_state: FrozenSet[Tuple[int, int]] = chamber.trim()
        min_chamber_state_size = min(min_chamber_state_size, len(chamber_state))
        max_chamber_state_size = max(max_chamber_state_size, len(chamber_state))
        state: Tuple[int, int, FrozenSet[Tuple[int, int]]] = (
            rock_index,
            wind_index,
            chamber_state,
        )
        if state in seen_state:
            break

        seen_state[state] = (current_number_of_rocks, chamber.size)

        current_number_of_rocks += 1

    previous_number_of_rocks, previous_chamber_size = seen_state[state]
    times: int = (number_of_rocks - current_number_of_rocks) // (
        current_number_of_rocks - previous_number_of_rocks
    )
    rocks_piles: int = (current_number_of_rocks - previous_number_of_rocks) * times
    size_reached: int = (chamber.size - previous_chamber_size) * times
    reminding_rocks: int = number_of_rocks - rocks_piles - current_number_of_rocks - 1

    current_number_of_rocks = 0
    while current_number_of_rocks < reminding_rocks:
        rock_index, rock = next(rocks)
        chamber.add_falling_rock(rock)

        while not chamber.is_stable():
            wind_index, wind = next(gas)
            chamber.gas_push(wind)
            chamber.fall_down()

        current_number_of_rocks += 1

    return chamber.size + size_reached


def parse(filename: str) -> List[Tuple[int, Wind]]:
    with open(filename, "r") as fp:
        raw_data: str = fp.read().strip()

    data: List[Tuple[int, Wind]] = []
    for index, char in enumerate(raw_data):
        data.append((index, get_wind_from_str(char)))

    return data


def solution(filename: str, number_of_rocks: int) -> int:
    wind_data: List[Tuple[int, Wind]] = parse(filename)
    chamber: Chamber = Chamber(7)

    return solve(wind_data, chamber, number_of_rocks)


if __name__ == "__main__":
    print(solution("./example.txt", 1_000_000_000_000))  # 1514285714288
    print(solution("./input.txt", 1_000_000_000_000))  # 1560932944615
