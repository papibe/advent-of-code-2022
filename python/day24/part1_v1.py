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
        # print(f"{rows = }, {cols = }")
        self.rows: int = rows
        self.cols: int = cols
        self.minute: int = 0
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
        new_blizzards: Dict = {}
        for direction in Blizzard.directions:
            new_blizzards[direction]: Dict = {}

        for direction, blizzards in self.blizzards.items():
            for bliz_row, bliz_col in blizzards:
                next_coord = (
                    (bliz_row - 1 + Blizzard.directions[direction][0]) % (self.rows - 2)
                    + 1,
                    (bliz_col - 1 + Blizzard.directions[direction][1]) % (self.cols - 2)
                    + 1,
                )
                new_blizzards[direction][next_coord] = True

        self.blizzards = new_blizzards
        self.minute += 1

    def is_free(self, coord) -> bool:
        if (
            coord[0] < 0
            or coord[0] >= self.rows
            or coord[1] < 0
            or coord[1] >= self.cols
        ):
            return False
        if coord in self.walls:
            return False
        for blizzards in self.blizzards.values():
            if coord in blizzards:
                return False
        return True

    def __eq__(self, __o: object) -> bool:
        # print(self.__hash__(),  __o.__hash__())
        return self.__hash__() == __o.__hash__()

    def __hash__(self) -> int:
        return hash(self.__repr__())

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

    return flat


def neighbors(coord: Tuple[int, int]) -> List:
    return [
        (coord[0] + step_row, coord[1] + step_col)
        for step_row, step_col in Blizzard.directions.values()
    ] + [coord]


def get_states(flat: Flat) -> int:
    visited: Set[Flat] = set([flat])
    states: List[Flat] = [deepcopy(flat)]
    for minute in range(1000):
        flat.next_state()
        if flat in visited:
            return states
        visited.add(flat)
        states.append(deepcopy(flat))

    return minute


def solve(
    minute: int,
    start: Tuple[int, int],
    end: Tuple[int, int],
    initial_state_number: int,
    states: List[Flat],
) -> int:
    visited: Set = set([(start, initial_state_number)])
    queue: Deque = deque([(start, initial_state_number, minute)])

    while queue:
        expedition, state_number, minute = queue.popleft()
        # print(minute, len(queue))
        flat = states[state_number]
        if expedition == end:
            return minute, state_number

        next_state_number = (state_number + 1) % len(states)
        next_state = states[next_state_number]

        for nb in neighbors(expedition):
            if (nb, next_state_number) in visited:
                # print("saving")
                continue
            if next_state.is_free(nb):
                # print("something")
                queue.append((nb, next_state_number, minute + 1))
                visited.add((nb, next_state_number))


def solution(filename: str) -> int:
    flat = parse(filename)
    states: List[Flat] = get_states(flat)
    # print(len(states))
    minute, state_number = solve(0, (0, 1), (flat.rows - 1, flat.cols - 2), 0, states)
    return minute

if __name__ == "__main__":
    print(solution("./example.txt"))
    print(solution("./input.txt"))
