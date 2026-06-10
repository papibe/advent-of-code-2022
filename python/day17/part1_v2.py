from enum import Enum
from typing import List, Tuple, Iterator, Dict, Set


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

STONE: str = "@"
ROCKS: List[List] = []

for rock in _ROCKS:
    rock_coordinates: List = []
    for i, row in enumerate(rock):
        for j, value in enumerate(row):
            # print(i, j, value, rock[i][j])
            if value == STONE:
                rock_coordinates.append((i, j))
    # print()
    ROCKS.append(rock_coordinates)


class Wind(Enum):
    left: str = "<"
    right: str = ">"


class Chamber:
    def __init__(self, width: int) -> None:
        self.chamber: Set = set()
        # for i in range(width):
        #     self.chamber.add((0, i))
        self.width: int = width
        self.size: int = 0
        self.size_wit_rock: int = 0
        self.stable: bool = True
        self.rock: Set = None

    def __repr__(self) -> str:
        # return f"{self.chamber = }\n{self.rock = }\n"

        # print(f"{self.size = }")
        output: List[str] = []
        for row in range(self.size + self.size_wit_rock - 1, -1, -1):
            output.append(f"{row:4} ")
            for col in range(self.width):
                if (row, col) in self.chamber:
                    output.append("#")
                elif self.rock is not None and (row, col) in self.rock:
                    output.append(STONE)
                else:
                    output.append(".")
            output.append("\n")
        return "".join(output)

    def add_falling_rock(self, rock: Tuple[Tuple]) -> None:

        # self.rock_row: int = self.size + (3 if self.size == 0 else 4)
        self.rock_row: int = self.size + 4
        self.rock_col: int = 2
        self.size_wit_rock: int = self.size + 4 + (4)

        # print(f"adding rock: {self.rock_row = } {self.rock_col = }")

        self.rock: Set = set()
        for x, y in rock:
            self.rock.add((self.rock_row + x, self.rock_col + y))

        # print(f"{self.rock = }")

        self.stable = False

    def _move_right(self):
        new_rock_position: Set = set()
        for (row, col) in self.rock:
            if col + 1 >= self.width or (row, col + 1) in self.chamber:
                return
            new_rock_position.add((row, col + 1))

        self.rock = new_rock_position

    def _move_left(self):
        new_rock_position: Set = set()
        for (row, col) in self.rock:
            if col - 1 < 0 or (row, col - 1) in self.chamber:
                return
            new_rock_position.add((row, col - 1))

        self.rock = new_rock_position

    # @profile
    def falldown(self):
        new_rock_position: Set = set()
        for (row, col) in self.rock:
            if row - 1 < 1 or (row - 1, col) in self.chamber:
                self.stabilize()
                return
            new_rock_position.add((row - 1, col))

        self.rock = new_rock_position

    def stabilize(self) -> None:
        max_row: int = float("-inf")

        for (row, col) in self.rock:
            max_row = max(max_row, row)
            self.chamber.add((row, col))

        self.rock = None
        self.size = max(max_row, self.size)
        self.size_wit_rock: int = max_row
        self.stable = True

    def gas_push(self, wind: str) -> None:
        wind_mapping: Dict = {Wind.left: self._move_left, Wind.right: self._move_right}
        wind_mapping[wind]()

    def is_stable(self) -> bool:
        return self.stable


def rock_generator(rocks_data: Tuple[Tuple]) -> Tuple:
    counter: int = 0
    rocks_length: int = len(rocks_data)
    while True:
        index: int = counter % rocks_length
        yield rocks_data[index]
        counter += 1


def wind_generator(wind_str: List[str]) -> Wind:
    counter: int = 0
    wind_length: int = len(wind_str)
    while True:
        index: int = counter % wind_length
        yield Wind.left if wind_str[index] == "<" else Wind.right
        counter += 1

# @profile
def solve(wind_data: List, chamber: Chamber, number_of_rocks: int) -> int:

    gas: Iterator = wind_generator(wind_data)
    rocks: Iterator = rock_generator(ROCKS)

    for nrocks in range(1, number_of_rocks + 1):
        rock = next(rocks)
        chamber.add_falling_rock(rock)
        # print("add rock")
        # print(chamber)

        while not chamber.is_stable():
            wind: str = next(gas)
            # print(wind)
            chamber.gas_push(wind)
            # print(chamber)
            chamber.falldown()
            # print("down")
            # print(chamber)

        # print(nrocks, chamber.size)
        # print(chamber)

    # for row in range(len(chamber.chamber) - 1, len(chamber.chamber) - 10, -1):
    #     print(chamber.chamber[row])

    # print(chamber)

    return chamber.size


def parse(filename: str):
    with open(filename, "r") as fp:
        raw_data: List = fp.read().splitlines()
    data: List[str] = [char for char in raw_data[0]]
    return data


def solution(filename: str, number_of_rocks: int) -> int:
    wind_data: List[str] = parse(filename)
    chamber: Chamber = Chamber(7)

    return solve(wind_data, chamber, number_of_rocks)


if __name__ == "__main__":
    result: int = solution("./example.txt", 2022)
    print(result)

    result = solution("./input.txt", 2022)
    print(result)
