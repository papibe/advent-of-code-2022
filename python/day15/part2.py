import re
from typing import Dict, Tuple, List

from part1 import Sensor, parse


def merge(intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort(key=lambda x: x[0])

    merged: List[List[int]] = [intervals[0]]
    for i in range(1, len(intervals)):
        if intervals[i][0] <= merged[-1][1] or merged[-1][-1] + 1 == intervals[i][0]:
            merged[-1][0] = min(merged[-1][0], intervals[i][0])
            merged[-1][1] = max(merged[-1][1], intervals[i][1])
        else:
            merged.append(intervals[i])
    return merged


def solution(sensors: Dict, beacon_in_row: Dict, row: int) -> int:
    # count intersections
    intersection_intervals: List[List[int]] = []
    for sensor in sensors.values():
        if sensor.lower_reach <= row <= sensor.high_reach:
            reminder_distance: int = sensor.manhattan_radius - abs(sensor.y - row)

            intersection: List[int] = [
                sensor.x - reminder_distance,
                sensor.x + reminder_distance,
            ]
            intersection_intervals.append(intersection)

    # merge all intervals
    merged_intervals: List[List[int]] = merge(intersection_intervals)

    if len(merged_intervals) == 1:
        return None

    return 4_000_000 * (merged_intervals[0][-1] + 1) + row


def solve(filename: int, max_row: int) -> int:
    sensors, beacon_in_row = parse(filename)

    for row in range(max_row + 1):
        result = solution(sensors, beacon_in_row, row)
        if result is not None:
            return result


if __name__ == "__main__":
    result: int = solve("./example.txt", 20)
    print(result)  # it should be 56000011

    result = solve("./input.txt", 4000000)
    print(result)
