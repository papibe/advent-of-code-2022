import re
from typing import Dict, Tuple, List


class Sensor:
    def __init__(
        self, sensor_x: int, sensor_y: int, beacon_x: int, beacon_y: int
    ) -> None:
        self.sensor_x: int = sensor_x
        self.sensor_y: int = sensor_y
        self.beacon_x: int = beacon_x
        self.beacon_y: int = beacon_y
        self.manhattan_radius: int = abs(beacon_x - sensor_x) + abs(sensor_y - beacon_y)
        self.lower_reach: int = sensor_y - self.manhattan_radius
        # self.lower_reach: int = (
        #     0
        #     if sensor_y - self.manhattan_radius < 0
        #     else sensor_y - self.manhattan_radius
        # )
        self.high_reach: int = sensor_y + self.manhattan_radius

    def __repr__(self) -> str:
        # return f"({self.sensor_x}, {self.sensor_y}) mr: {self.manhattan_radius}"
        return f"({self.sensor_x}, {self.sensor_y}) radius: {self.manhattan_radius} reach: {self.lower_reach}, {self.high_reach}"


class Beacon:
    def __init__(
        self, sensor_x: int, sensor_y: int, beacon_x: int, beacon_y: int
    ) -> None:
        self.sensor_x: int = sensor_x
        self.sensor_y: int = sensor_y
        self.beacon_x: int = beacon_x
        self.beacon_y: int = beacon_y
        self.manhattan_radius: int = abs(beacon_x - sensor_x) + abs(sensor_y - beacon_y)

    def __repr__(self) -> str:
        return f"({self.beacon_x}, {self.beacon_y}) mr: {self.manhattan_radius}"


def merge(intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort(key=lambda x: x[0])

    merged: List[List[int]] = [intervals[0]]  # 1 <= intervals.length <= 10^
    for i in range(1, len(intervals)):
        if intervals[i][0] <= merged[-1][1] or merged[-1][-1] + 1 == intervals[i][0]:
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
    beacons: Dict[Tuple[int, int], Sensor] = {}
    for line in data:
        result = re.match(expr, line)
        sensor_x = int(result.group(1))
        sensor_y = int(result.group(2))
        beacon_x = int(result.group(3))
        beacon_y = int(result.group(4))

        sensors[(sensor_x, sensor_y)] = Sensor(sensor_x, sensor_y, beacon_x, beacon_y)
        beacons[(beacon_x, beacon_y)] = Beacon(sensor_x, sensor_y, beacon_x, beacon_y)

    return sensors, beacons


def solution(sensors: Dict, beacons: Dict, row: int) -> int:

    # Check if there's a beacon on the row
    for (beacon_x, beacon_y), beacon in beacons.items():
        if beacon_y == row:
            return None

    # count intersections
    intersections: List[List[int]] = []
    for (sensor_x, sensor_y), sensor in sensors.items():
        # print(sensor_x, sensor_y, sensor)

        if sensor.lower_reach <= row <= sensor.high_reach:
            distance_from_sensor: int = abs(sensor_y - row)
            reminder_distance: int = sensor.manhattan_radius - distance_from_sensor
            intersection_length: int = reminder_distance * 2 + 1

            # print(
            #     f"{distance_from_sensor = } {reminder_distance = } {intersection_length = }"
            # )

            intersection: List[int] = [
                sensor_x - reminder_distance,
                sensor_x + reminder_distance,
            ]
            # print(intersection)
            intersections.append(intersection)

        # print("=" * 50)


    merged_intervals: List[List[int]] = merge(intersections)

    if len(merged_intervals) == 1:
        return None
        # print(row, merged_intervals)

    return 4_000_000 * (merged_intervals[0][-1] + 1) + row

def solve(filename: int, max_row: int) -> int:
    sensors, beacons = parse(filename)

    for row in range(max_row + 1):
        # if row % 10_000 == 0:
        #     print(row)
        result = solution(sensors, beacons, row)
        if result is not None:
            return result


if __name__ == "__main__":
    # result: int = solve("./example.txt", 20)
    # print(result)  # it should be 56000011

    result: int = solve("./input.txt", 4000000)
    print(result)
