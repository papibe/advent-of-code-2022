import re
from collections import namedtuple
from typing import List, Match, Optional, Set, Tuple

LAST: int = -1

Interval = namedtuple("Interval", ["start", "end"])


class Sensor:
    def __init__(
        self, sensor_x: int, sensor_y: int, beacon_x: int, beacon_y: int
    ) -> None:
        self.x: int = sensor_x
        self.y: int = sensor_y
        self.beacon_x: int = beacon_x
        self.beacon_y: int = beacon_y
        self.manhattan_radius: int = abs(beacon_x - sensor_x) + abs(sensor_y - beacon_y)
        self.lower_reach: int = sensor_y - self.manhattan_radius
        self.high_reach: int = sensor_y + self.manhattan_radius

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}) radius: {self.manhattan_radius} reach: {self.lower_reach}, {self.high_reach}"


class Beacon:
    def __init__(self, beacon_x: int, beacon_y: int) -> None:
        self.x: int = beacon_x
        self.y: int = beacon_y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Beacon):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


def merge(intervals: List[Interval]) -> List[Interval]:
    intervals.sort(key=lambda x: x.start)
    merged: List[Interval] = [intervals[0]]  # 1 <= intervals.length <= 10^

    for i in range(1, len(intervals)):
        if intervals[i].start <= merged[-1].end:
            merged[LAST] = Interval(
                min(merged[LAST].start, intervals[i].start),
                max(merged[LAST].end, intervals[i].end),
            )
        else:
            merged.append(intervals[i])

    return merged


def parse(filename: str) -> Tuple[List[Sensor], Set[Beacon]]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    expr: str = (
        r"Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)"
    )

    sensors: List[Sensor] = []
    beacons: Set[Beacon] = set()

    for line in data:
        result: Optional[Match[str]] = re.match(expr, line)
        if result:
            sensor_x: int = int(result.group(1))
            sensor_y: int = int(result.group(2))
            beacon_x: int = int(result.group(3))
            beacon_y: int = int(result.group(4))

        sensors.append(Sensor(sensor_x, sensor_y, beacon_x, beacon_y))
        beacons.add(Beacon(beacon_x, beacon_y))

    return sensors, beacons


def solve(
    sensors: List[Sensor],
    beacons: Set[Beacon],
    row: int,
) -> int:

    # count intersections
    intersections: List[Interval] = []

    for sensor in sensors:
        if sensor.lower_reach <= row <= sensor.high_reach:
            distance_from_sensor: int = abs(sensor.y - row)
            reminder_distance: int = sensor.manhattan_radius - distance_from_sensor

            intersection: Interval = Interval(
                sensor.x - reminder_distance,
                sensor.x + reminder_distance,
            )
            intersections.append(intersection)

    merged_intervals: List[Interval] = merge(intersections)

    total_intersections: int = sum(
        [(interval[1] - interval[0] + 1) for interval in merged_intervals]
    )
    # subtract beacons on the row `row`
    for beacon in beacons:
        if beacon.y == row:
            for start, end in merged_intervals:
                if start <= beacon.x <= end:
                    total_intersections -= 1
    return total_intersections


def solution(filename: str, row: int) -> int:
    sensors, beacons = parse(filename)
    return solve(sensors, beacons, row)


if __name__ == "__main__":
    print(solution("./example.txt", 10))  # 26
    print(solution("./input.txt", 2_000_000))  # 4724228
