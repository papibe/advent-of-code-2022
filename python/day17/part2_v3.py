from enum import Enum
from collections import deque
from typing import FrozenSet, List, Tuple, Iterator, Dict, Set, Deque


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
                # self.trim()
                return
            new_rock_position.add((row - 1, col))

        self.rock = new_rock_position

    def trim(self) -> Set:
        upper_limit: int = self.size + 1
        start: Tuple = (upper_limit, 0)
        queue: Deque = deque([start])
        visited: Set = {start}

        new_chamber: Set = set()
        min_row: int = float("inf")

        while queue:
            row, col = queue.popleft()
            if (row, col) in self.chamber:
                new_chamber.add((row, col))
                continue
            for drow, dcol in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                if 0 < row + drow <= upper_limit and 0 <= col + dcol < self.width:
                    if (row + drow, col + dcol) not in visited:
                        queue.append((row + drow, col + dcol))
                        visited.add((row + drow, col + dcol))

                        min_row = min(min_row, row + drow)

        self.chamber = new_chamber

        state: Set = set()
        for row, col in new_chamber:
            state.add((row - min_row, col))

        return frozenset(state)

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
        yield (index, rocks_data[index])
        counter += 1


def wind_generator(wind_str: List[str]) -> Wind:
    counter: int = 0
    wind_length: int = len(wind_str)
    while True:
        index: int = counter % wind_length
        wind: Wind = Wind.left if wind_str[index] == "<" else Wind.right
        yield (index, wind)
        counter += 1


# @profile
def solve(wind_data: List, chamber: Chamber, number_of_rocks: int) -> int:

    seen_state: Dict = {}
    min_chamber_state_size: int = float("inf")
    max_chamber_state_size: int = float("-inf")

    gas: Iterator = wind_generator(wind_data)
    rocks: Iterator = rock_generator(ROCKS)

    nrocks: int = 0
    while nrocks < number_of_rocks:
    # for nrocks in range(1, number_of_rocks + 1):
        rock_index, rock = next(rocks)
        chamber.add_falling_rock(rock)
        # print("add rock")
        # print(chamber)

        while not chamber.is_stable():
            wind_index, wind = next(gas)
            # print(wind)
            chamber.gas_push(wind)
            # print(chamber)
            chamber.falldown()
            # print("down")
            # print(chamber)

        chamber_state: FrozenSet = chamber.trim()
        min_chamber_state_size = min(min_chamber_state_size, len(chamber_state))
        max_chamber_state_size = max(max_chamber_state_size, len(chamber_state))
        state: Tuple = (rock_index, wind_index, chamber_state)
        if state in seen_state:
            # if len(chamber_state) == 7 and chamber_state == frozenset(
            #     {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)}
            # ):
            #     print(nrocks, "flat!")
            # print(chamber_state)
            # break
            break
            pass
        else:
            # print("New state V")
            seen_state[state] = (nrocks, chamber.size)  # nrocks diff?

        nrocks += 1

    print(f"Repetition: at {nrocks = }")
    print(f"current size {chamber.size = }")
    previous_nrocks, previous_chamber_size = seen_state[state]
    print(f"{previous_nrocks = }, {previous_chamber_size = }")

    # times: int = ((number_of_rocks - previous_chamber_size) // (nrocks - previous_nrocks))
    times: int = ((number_of_rocks - nrocks) // (nrocks - previous_nrocks))
    print(f"clycle can repeat {times = }")

    nrocks_piles: int = (nrocks - previous_nrocks) * times
    print(f"rocks that can be piled {nrocks_piles = }")
    size_reached: int = (chamber.size - previous_chamber_size) * times
    # size_reached: int = (chamber.size - previous_chamber_size) * times
    print(f"{size_reached = }")

    reminding_rocks: int = number_of_rocks - nrocks_piles - nrocks - 1
    print(f"reminding rocks {reminding_rocks = }")

    # chamber.size += nrocks_piles

    current_nrocks: int = 0 
    # current_nrocks: int = nrocks_piles
    # while current_nrocks < number_of_rocks:
    while current_nrocks < reminding_rocks:
    # for nrocks in range(1, number_of_rocks + 1):
        rock_index, rock = next(rocks)
        chamber.add_falling_rock(rock)
        # print("add rock")
        # print(chamber)

        while not chamber.is_stable():
            wind_index, wind = next(gas)
            # print(wind)
            chamber.gas_push(wind)
            # print(chamber)
            chamber.falldown()
            # print("down")
            # print(chamber)

        current_nrocks += 1

    # print("states seen", len(seen_state))
    # print("min state", min_chamber_state_size)
    print(f"{chamber.size = }")
    return chamber.size + size_reached


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
    result: int = solution("./example.txt", 1_000_000_000_000)
    # result: int = solution("./example.txt", 2022)
    # result: int = solution("./example.txt", 100_000)
    # result: int = solution("./example.txt", 10)
    print(result)

    # result = solution("./input.txt", 2022)
    # result = solution("./input.txt", 100_000)
    result: int = solution("./input.txt", 1_000_000_000_000)
    print(result)
