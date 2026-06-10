import re
import math
from typing import List, Set, Tuple


class Plank:
    def __init__(self) -> None:
        self.x: int = 0
        self.y: int = 0

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

    def follow(self, head) -> None:
        if abs(self.x - head.x) <= 1 and abs(self.y - head.y) <= 1:
            return

        if abs(self.x - head.x) == 2 and self.y == head.y:
            self.x += int(math.copysign(1, head.x - self.x))

        elif abs(head.y - self.y) == 2 and self.x == head.x:
            self.y += int(math.copysign(1, head.y - self.y))

        elif abs(self.x - head.x) == 2 and abs(head.y - self.y) == 1:
            self.x += int(math.copysign(1, head.x - self.x))
            self.y = head.y
        # new case for part 2
        elif abs(self.y - head.y) == 2 and abs(head.x - self.x) == 1:
            self.x = head.x
            self.y += int(math.copysign(1, head.y - self.y))


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        motions: List[str] = fp.read().splitlines()

    head: Plank = Plank()
    tail: Plank = Plank()
    visited: Set[Tuple[int, int]] = {(0, 0)}

    for raw_motion in motions:
        exp = re.match("(\w) (\d+)", raw_motion)
        direction = exp.group(1)
        amount = int(exp.group(2))

        # move head one step at a time
        for _ in range(amount):
            head.move(direction)
            tail.follow(head)
            visited.add(tail.get_pos())

    return len(visited)


if __name__ == "__main__":
    result: int = solution("./data/example1.txt")
    print(result)  # it should be 13

    result = solution("./data/input.txt")
    print(result)
