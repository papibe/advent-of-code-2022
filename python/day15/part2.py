import re
from typing import List, Match, Optional, Tuple

MULTIPLIER: int = 4_000_000


class Sensor:
    def __init__(
        self, sensor_x: int, sensor_y: int, beacon_x: int, beacon_y: int
    ) -> None:
        self.x: int = sensor_x
        self.y: int = sensor_y
        self.manhattan_radius: int = abs(beacon_x - sensor_x) + abs(sensor_y - beacon_y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}) radius: {self.manhattan_radius}"


def parse(filename: str) -> List[Sensor]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    expr: str = (
        r"Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)"
    )

    sensors: List[Sensor] = []
    for line in data:
        result: Optional[Match[str]] = re.match(expr, line)
        if result:
            sensor_x: int = int(result.group(1))
            sensor_y: int = int(result.group(2))
            beacon_x: int = int(result.group(3))
            beacon_y: int = int(result.group(4))
        sensors.append(Sensor(sensor_x, sensor_y, beacon_x, beacon_y))

    return sensors


def solve(sensors: List[Sensor], max_dimension: int) -> int:
    n: int = len(sensors)
    adjacent: List[Tuple[Sensor, Sensor]] = []
    for i in range(n):
        for j in range(i + 1, n):
            s1: Sensor = sensors[i]
            s2: Sensor = sensors[j]
            distance: int = abs(s1.x - s2.x) + abs(s1.y - s2.y)
            if distance == (s1.manhattan_radius + s2.manhattan_radius + 2):
                adjacent.append((s1, s2))

    # input has only 2 pairs, however example has multiple matching pairs
    adjacent = adjacent[:2]

    # determine coordinates of the diagonals
    left: Sensor
    right: Sensor
    sign: int
    x: int
    y: int
    coords: List[Tuple[int, int, int]] = []

    for s1, s2 in adjacent:
        if s1.x < s2.x:
            left = s1
            right = s2
        else:
            left = s2
            right = s1

        if left.y > right.y:
            x, y = left.x, left.y - left.manhattan_radius - 1
            sign = -1
        else:
            x, y = left.x, left.y + left.manhattan_radius + 1
            sign = 1

        coords.append((x, y, sign))

    (x1, y1, sign1), (x2, y2, sign2) = coords

    # solve intersections of diagonals
    x = (x1 + sign1 * y1 + x2 + sign2 * y2) // 2
    y = -(x1 + sign1 * y1 - x2 - sign2 * y2) // 2

    assert 0 <= x <= max_dimension and 0 <= y <= max_dimension

    return (MULTIPLIER * x) + y


def solution(filename: str, row: int) -> int:
    sensors: List[Sensor] = parse(filename)
    return solve(sensors, row)


if __name__ == "__main__":
    print(solution("./example.txt", 20))  # 56000011
    print(solution("./input.txt", 4_000_000))  # 13622251246513
