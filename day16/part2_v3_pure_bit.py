import itertools
import re
from collections import deque
from typing import List, Dict, Deque, Set, Tuple


class Valve:
    def __init__(
        self, name: str, flow: int = None, neighbors: List[str] = None
    ) -> None:
        self.name: str = name
        self.flow: int = flow
        self.neighbors: List[str] = neighbors

    def __repr__(self) -> str:
        return f"name: {self.name}, flow: {self.flow}, neighbors: {self.neighbors}"


def parse(filename: str) -> Dict[str, Valve]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    valves: Dict[str, Valve] = {}
    pattern: str = r"Valve (\w+) has flow rate=(\d+); tunnels* leads* to valves* (.*)$"
    for line in data:
        match_expr = re.match(pattern, line)
        valve_name: str = match_expr.group(1)
        valve_flow: int = int(match_expr.group(2))
        connecting_valves: List[str] = [
            valve.strip() for valve in match_expr.group(3).split(",")
        ]

        valves[valve_name] = Valve(valve_name, valve_flow, connecting_valves)

    return valves


def solve(
    valves: Dict[str, Valve],
    valve_index: Dict,
    opened_valves: int,
    memo: Dict,
    max_minutes: int,
) -> int:
    def sol(minutes: int, valve: str, opened: Set):
        if minutes == 0:
            return 0

        if (minutes, valve, opened) in memo:
            return memo[(minutes, valve, opened)]

        max_pressure = max(
            [sol(minutes - 1, neighbor, opened) for neighbor in valves[valve].neighbors]
        )

        if valves[valve].flow > 0:
            valve_bit = 1 << valve_index[valve]
            if opened & valve_bit == 0:  # not opened
                max_pressure = max(
                    max_pressure,
                    valves[valve].flow * (minutes - 1)
                    + sol(minutes - 1, valve, opened | valve_bit),
                )

        memo[(minutes, valve, opened)] = max_pressure
        return max_pressure

    return sol(max_minutes, "AA", opened_valves)


def solution(filename: str) -> int:
    valves: Dict[Valve] = parse(filename)

    good_valves = [valve for valve in valves if valves[valve].flow > 0]
    valve_index: Dict[str, int] = {valve: i for i, valve in enumerate(good_valves)}

    memo: Dict = {}

    max_team_preassure: int = 0
    times: int = (2 ** len(good_valves)) - 1
    for bitmask in range(times //  2):
        player2_preassure: int = solve(
            valves, valve_index, bitmask, memo, 26
        )
        player1_preassure: int = solve(
            valves, valve_index, bitmask ^ times, memo, 26
        )

        max_team_preassure = max(
            max_team_preassure, player1_preassure + player2_preassure
        )

    return max_team_preassure


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)

    result = solution("./input.txt")
    print(result)   # ~ 3m20s
