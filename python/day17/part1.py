from enum import Enum
from typing import List, Tuple, Iterator, Dict


ROCKS = (
    (("@", "@", "@", "@"),),
    (
        (".", "@", "."),
        ("@", "@", "@"),
        (".", "@", "."),
    ),
    (
        (".", ".", "@"),
        (".", ".", "@"),
        ("@", "@", "@"),
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


class Wind(Enum):
    left: str = "<"
    right: str = ">"


class Chamber:
    def __init__(self) -> None:
        self.chamber: List[str] = [["#"] * 7]
        # self.height: int = 0
        self.size: int = 1
        self.falling_rock: Tuple[Tuple] = None
        self.falling_rock_row: int = None
        self.falling_rock_col: int = None
        self.stable: bool = True

    def __repr__(self) -> str:
        output: List[str] = []
        # draw chamber with stopped rocks
        # print(f"{self.size = } {len(self.chamber) = }")
        for row_index in range(self.size - 1, -1, -1):
            output.append(f"{row_index:4} ")
            for col_index in range(7):
                output.append(self.chamber[row_index][col_index])
            output.append("\n")
        return "".join(output)

    def add_falling_rock(self, rock: Tuple[Tuple]) -> None:
        for _ in range(3 + len(rock)):
            self.chamber.append(["."] * 7)
        # self.size += 4 + len(rock) - 1
        self.size = len(self.chamber)
        # print(f"{self.size = } {len(self.chamber) = }")

        self.falling_rock_row: int = self.size - len(rock)
        self.falling_rock_col: int = 2
        self.falling_rock = rock

        # print(f"adding rock: {self.falling_rock_row = } {self.falling_rock_col = }")

        for i, rock_row in enumerate(rock):
            for j, stone in enumerate(rock_row):
                self.chamber[self.size - 1 - i][self.falling_rock_col + j] = stone

        self.stable = False

    def _move_left(self):
        # print("moving left")
        # check if move is possible
        for i in range(
            self.falling_rock_row, self.falling_rock_row + len(self.falling_rock)
        ):
            for j in range(
                self.falling_rock_col, self.falling_rock_col + len(self.falling_rock[0])
            ):
                # hit a wall and that's ok
                if j - 1 < 0:
                    return
                # print(i, j)
                if self.chamber[i][j] == "@" and self.chamber[i][j - 1] == "#":
                    # print(i, j, f"{self.chamber[i][j] = } {self.chamber[i][j - 1] = }")
                    return
        # do the move
        for i in range(
            self.falling_rock_row, self.falling_rock_row + len(self.falling_rock)
        ):
            for j in range(
                self.falling_rock_col, self.falling_rock_col + len(self.falling_rock[0])
            ):
                self.chamber[i][j], self.chamber[i][j - 1] = (
                    self.chamber[i][j - 1],
                    self.chamber[i][j],
                )

        self.falling_rock_col -= 1

    def _move_right(self):
        # check if move is possible
        for i in range(
            self.falling_rock_row, self.falling_rock_row + len(self.falling_rock)
        ):
            for j in range(
                self.falling_rock_col, self.falling_rock_col + len(self.falling_rock[0])
            ):
                # hit a wall and that's ok
                if j + 1 >= 7:
                    return
                if self.chamber[i][j] == "@" and self.chamber[i][j + 1] == "#":
                    # print(i, j, f"{self.chamber[i][j] = } {self.chamber[i][j + 1] = }")
                    return
        # do the move
        # print("moving right now")
        for i in range(
            self.falling_rock_row, self.falling_rock_row + len(self.falling_rock)
        ):
            for j in range(
                self.falling_rock_col + len(self.falling_rock[0]) - 1,
                self.falling_rock_col - 1,
                -1,
            ):
                self.chamber[i][j], self.chamber[i][j + 1] = (
                    self.chamber[i][j + 1],
                    self.chamber[i][j],
                )
        self.falling_rock_col += 1

    def gas_push(self, wind: str) -> None:
        # print(f"{wind = }")
        wind_mapping: Dict = {Wind.left: self._move_left, Wind.right: self._move_right}
        wind_mapping[wind]()

    def falldown(self) -> None:
        # check if move is possible
        # print("down")
        for i in range(
            self.falling_rock_row, self.falling_rock_row + len(self.falling_rock)
        ):
            for j in range(
                self.falling_rock_col, self.falling_rock_col + len(self.falling_rock[0])
            ):
                # hit a wall and that's ok
                if i - 1 < 0 or (
                    self.chamber[i][j] == "@" and self.chamber[i - 1][j] == "#"
                ):
                    # print(i, j, f"{self.chamber[i][j] = } {self.chamber[i][j + 1] = }")
                    self.stabilize()
                    return
        # do the move
        # print("moving down now")
        for i in range(
            self.falling_rock_row, self.falling_rock_row + len(self.falling_rock)
        ):
            for j in range(
                self.falling_rock_col, self.falling_rock_col + len(self.falling_rock[0])
            ):
                self.chamber[i][j], self.chamber[i - 1][j] = (
                    self.chamber[i - 1][j],
                    self.chamber[i][j],
                )
        self.falling_rock_row -= 1

    def stabilize(self) -> None:
        for i in range(
            self.falling_rock_row, self.falling_rock_row + len(self.falling_rock)
        ):
            for j in range(
                self.falling_rock_col,
                self.falling_rock_col + len(self.falling_rock[0]),
            ):
                if self.chamber[i][j] == "@":
                    self.chamber[i][j] = "#"
        # trim hall/cavern
        while "".join(self.chamber[-1]) == ".......":
            self.chamber.pop()
            self.size -= 1

        self.stable = True

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


def parse(filename: str):
    with open(filename, "r") as fp:
        raw_data: List = fp.read().splitlines()
    data: List[str] = [char for char in raw_data[0]]
    return data


def solve(wind_data: List, chamber: Chamber, number_of_rocks: int) -> int:
    # chamber.add_falling_rock(ROCKS[0])
    # print(chamber)

    gas: Iterator = wind_generator(wind_data)

    for nrocks, rock in enumerate(rock_generator(ROCKS)):
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

        # print(nrocks + 1, chamber.size - 1, len(chamber.chamber))
        # print(chamber)
        # if nrocks + 1 == number_of_rocks:
        # if nrocks + 1 == 10:
            # chamber.add_falling_rock(rock)
            # break

    # for row in range(len(chamber.chamber) - 1, len(chamber.chamber) - 10, -1):
    #     print(chamber.chamber[row])

    # print(chamber)

    return chamber.size - 1


def solution(filename: str, number_of_rocks: int) -> int:
    wind_data: List[str] = parse(filename)
    # print(len(wind_data), wind_data[0], wind_data[-1])
    # print(wind_data)
    # for wind in wind_generator(wind_data):
    #     print(wind)
    chamber: Chamber = Chamber()
    return solve(wind_data, chamber, number_of_rocks)


if __name__ == "__main__":
    result: int = solution("./example.txt", 2022)
    print(result)

    # result = solution("./input.txt", 2022)
    # print(result)
