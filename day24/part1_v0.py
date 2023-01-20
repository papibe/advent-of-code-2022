from collections import deque
from copy import deepcopy
from typing import List, Dict, Tuple, Set, Deque


class Blizzard:
    directions: Dict[str, Tuple[int, int]] = {
        "^": (-1, 0),
        "v": (1, 0),
        ">": (0, 1),
        "<": (0, -1),
    }

    def __init__(self, direction: str, coord: Tuple[int, int]) -> None:
        self.direction: str = direction
        self.coord: Tuple[int, int] = coord


class Flat:
    def __init__(self, rows: int, cols: int) -> None:
        print(f"{rows = }, {cols = }")
        self.rows: int = rows
        self.cols: int = cols
        self.expedition: Tuple[int, int] = (0, 1)
        self.finish: Tuple[int, int] = (self.rows - 1, self.cols - 2)
        self.walls: Set[Tuple[int, int]] = set()

        self.blizzards: Dict = {}
        for direction in Blizzard.directions:
            self.blizzards[direction]: Dict = {}

    def add_wall(self, coord: Tuple[int, int]) -> None:
        self.walls.add(coord)

    def add_blizzard(self, direction: str, coord: Tuple[int, int]) -> None:
        self.blizzards[direction][coord] = True

    def next_state(self) -> None:
        # for blizzards in (self.up_blizzards, self.down_blizzards, self.left_blizzards, self.right_blizzards):
        # TODO: here
        new_blizzards: Dict = {}
        for direction in Blizzard.directions:
            new_blizzards[direction]: Dict = {}

        for direction, blizzards in self.blizzards.items():
            for bliz_row, bliz_col in blizzards:
                next_coord = (
                    (bliz_row - 1 + Blizzard.directions[direction][0]) % (self.rows - 2) + 1,
                    (bliz_col - 1 + Blizzard.directions[direction][1]) % (self.cols - 2) + 1
                )
                new_blizzards[direction][next_coord] = True
            
        self.blizzards = new_blizzards

    def __repr__(self) -> str:
        output: List[str] = []
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in self.walls:
                    output.append("#")
                    continue
                if (row, col) == self.finish:
                    output.append("F")
                    continue
                if (row, col) == self.expedition:
                    output.append("E")
                    continue

                candidate: List[str] = ["."]
                for direction in self.blizzards:
                    if (row, col) in self.blizzards[direction]:
                        candidate.append(direction)
                if len(candidate) == 1:
                    output.append(".")
                elif len(candidate) == 2:
                    output.append(candidate[1])
                else:
                    output.append(str(len(candidate) - 1))

            output.append("\n")
        return "".join(output)


def parse(filename: str) -> Dict:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    flat: Flat = Flat(len(data), len(data[0]))
    for row, line in enumerate(data):
        for col, item in enumerate(line):
            if item == ".":
                continue
            elif item == "#":
                flat.add_wall((row, col))
            else:
                flat.add_blizzard(item, (row, col))

            # if item == "^":
            #     flat.add_up_blizzard((row, col))
            # if item == "V":
            #     flat.add_down_blizzard((row, col))
            # if item == ">":
            #     flat.add_right_blizzard((row, col))
            # if item == "<":
            #     flat.add_left_blizzard((row, col))

    return flat


def solve(initial_flat: Flat) -> int:
    visited: Set = set()
    queue: Deque = deque()
    queue.append(initial_flat)

    while queue:
        flat: Flat = queue.popleft()
        print(flat)
        flat.next_state()
        print(flat)
        break


def solution(filename: str) -> int:
    flat = parse(filename)
    return solve(flat)


if __name__ == "__main__":
    print(solution("./example.txt"))
    # print(solution("./input.txt"))
