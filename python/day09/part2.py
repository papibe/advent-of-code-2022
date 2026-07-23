import math
import re
from collections import namedtuple
from typing import List, Match, Optional, Set, Tuple

LAST: int = -1

Instruction = namedtuple("Instruction", ["direction", "amount"])


class Plank:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def get_pos(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def move(self, direction: str) -> None:
        if direction == "R":
            self.x += 1
        elif direction == "U":
            self.y += 1
        elif direction == "L":
            self.x -= 1
        elif direction == "D":
            self.y -= 1

    def follow(self, head: "Plank") -> None:
        if abs(self.x - head.x) <= 1 and abs(self.y - head.y) <= 1:
            return

        if abs(self.x - head.x) == 2 and self.y == head.y:
            self.x += int(math.copysign(1, head.x - self.x))

        elif abs(head.y - self.y) == 2 and self.x == head.x:
            self.y += int(math.copysign(1, head.y - self.y))

        elif abs(self.x - head.x) == 2 and abs(head.y - self.y) == 1:
            self.x += int(math.copysign(1, head.x - self.x))
            self.y = head.y

        elif abs(self.y - head.y) == 2 and abs(head.x - self.x) == 1:
            self.x = head.x
            self.y += int(math.copysign(1, head.y - self.y))

        elif abs(self.y - head.y) == 2 and abs(head.x - self.x) == 2:
            self.x += int(math.copysign(1, head.x - self.x))
            self.y += int(math.copysign(1, head.y - self.y))


def parse(filename: str) -> List[Instruction]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    instructions: List[Instruction] = []

    for line in data:
        matches: Optional[Match[str]] = re.match(r"(\w) (\d+)", line)
        if matches:
            direction: str = matches.group(1)
            amount: int = int(matches.group(2))
            instructions.append(Instruction(direction, amount))

    return instructions


def solve(instructions: List[Instruction]) -> int:
    rope: List[Plank] = [Plank(0, 0) for _ in range(10)]
    head: Plank = rope[0]
    tail: Plank = rope[LAST]
    visited: Set[Tuple[int, int]] = {(0, 0)}

    for instr in instructions:
        # move head on step at a time
        for _ in range(instr.amount):
            head.move(instr.direction)

            # move each knot based on the next ahead of it
            for index in range(1, 10):
                rope[index].follow(rope[index - 1])

            visited.add(tail.get_pos())

    return len(visited)


def solution(filename: str) -> int:
    instructions: List[Instruction] = parse(filename)
    return solve(instructions)


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 1
    print(solution("./example2.txt"))  # 36
    print(solution("./input.txt"))  # 2376
