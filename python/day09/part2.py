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

        elif abs(self.y - head.y) == 2 and abs(head.x - self.x) == 1:
            self.x = head.x
            self.y += int(math.copysign(1, head.y - self.y))

        elif abs(self.y - head.y) == 2 and abs(head.x - self.x) == 2:
            self.x += int(math.copysign(1, head.x - self.x))
            self.y += int(math.copysign(1, head.y - self.y))


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        motions: List[str] = fp.read().splitlines()

    rope = [Plank() for _ in range(10)]
    head: Plank = rope[0]
    tail: Plank = rope[-1]
    visited: Set[Tuple[int, int]] = {(0, 0)}

    for raw_motion in motions:
        exp = re.match("(\w) (\d+)", raw_motion)
        direction = exp.group(1)
        amount = int(exp.group(2))

        # move head on step at a time
        for _ in range(amount):
            head.move(direction)

            # move each knot based on the next ahed of it
            for index in range(1, 10):
                rope[index].follow(rope[index - 1])

            visited.add(tail.get_pos())

    return len(visited)


if __name__ == "__main__":
    result: int = solution("./data/example1.txt")
    print(result)  # it should be 1

    result: int = solution("./data/example2.txt")
    print(result)  # it should be 36

    result = solution("./data/input.txt")
    print(result)
