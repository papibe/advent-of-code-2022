import re
from typing import Dict, Tuple, List, Set


class Sensor:
    def __init__(
        self, sensor_x: int, sensor_y: int, beacon_x: int, beacon_y: int
    ) -> None:
        self.x: int = sensor_x
        self.y: int = sensor_y
        self.manhattan_radius: int = abs(beacon_x - sensor_x) + abs(sensor_y - beacon_y)
        self.lower_reach: int = sensor_y - self.manhattan_radius
        self.high_reach: int = sensor_y + self.manhattan_radius


def merge(intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort(key=lambda x: x[0])

    merged: List[List[int]] = [intervals[0]]
    for i in range(1, len(intervals)):
        if intervals[i][0] <= merged[-1][1]:
            merged[-1][0] = min(merged[-1][0], intervals[i][0])
            merged[-1][1] = max(merged[-1][1], intervals[i][1])
        else:
            merged.append(intervals[i])
    return merged


def parse(filename: int) -> Tuple[Dict, Dict]:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    expr = r"Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)"

    # parse input and create sensors and beacons dictionaries
    sensors: Dict[Tuple[int, int], Sensor] = {}
    beacon_in_row: Dict[int, Set[int]] = {}
    for line in data:
        result = re.match(expr, line)
        sensor_x = int(result.group(1))
        sensor_y = int(result.group(2))
        beacon_x = int(result.group(3))
        beacon_y = int(result.group(4))

        sensors[(sensor_x, sensor_y)] = Sensor(sensor_x, sensor_y, beacon_x, beacon_y)
        if beacon_y in beacon_in_row:
            beacon_in_row[beacon_y].add(beacon_x)
        else:
            beacon_in_row[beacon_y] = set([beacon_x])

    return sensors, beacon_in_row


def solution(filename: str, row: int) -> int:
    sensors, beacon_in_row = parse(filename)

    # count intersections
    intersection_intervals: List[List[int]] = []
    for sensor in sensors.values():
        if sensor.lower_reach <= row <= sensor.high_reach:
            distance_from_sensor: int = abs(sensor.y - row)
            reminder_distance: int = sensor.manhattan_radius - distance_from_sensor

            intersection: List[int] = [
                sensor.x - reminder_distance,
                sensor.x + reminder_distance,
            ]
            intersection_intervals.append(intersection)

    # merge all intervals
    merged_intervals: List[List[int]] = merge(intersection_intervals)

    # calculate all intersection points
    total_intersections: int = sum(
        [(interval[1] - interval[0] + 1) for interval in merged_intervals]
    )

    # substract beacons that are on the row `row`
    total_intersections -= len(beacon_in_row.get(row, dict()))
    return total_intersections


if __name__ == "__main__":
    result: int = solution("./example.txt", 10)
    print(result)  # it should be 26

    result = solution("./input.txt", 2_000_000)
    print(result)
