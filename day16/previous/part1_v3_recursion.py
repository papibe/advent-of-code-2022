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

    # need it?
    def update_flow_and_neighbors(self, flow: int, neighbors: List[str]) -> None:
        self.flow: int = flow
        self.neighbors: List[str] = neighbors

    def __repr__(self) -> str:
        return f"name: {self.name}, flow: {self.flow}, neighbors: {self.neighbors}"


def parse(filename: str) -> Dict[str, Valve]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    valves: Dict[str, Valve] = {}
    pattern: str = r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)$"
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
    opened_valves_setup: Set[str],
    memo: Dict,
    max_minutes: int,
) -> int:
    def sol(minutes: int, valve: str, opened: Set):
        if minutes == 0:
            return 0

        if (minutes, valve, frozenset(opened)) in memo:
            return memo[(minutes, valve, frozenset(opened))]

        max_pressure = max(
            [sol(minutes - 1, neighbor, opened) for neighbor in valves[valve].neighbors]
        )

        if valves[valve].flow > 0 and valve not in opened:
            new_opened = opened.copy()
            new_opened.add(valve)
            max_pressure = max(
                max_pressure,
                valves[valve].flow * (minutes - 1)
                + sol(minutes - 1, valve, new_opened),
            )

        memo[(minutes, valve, frozenset(opened))] = max_pressure
        return max_pressure

    return sol(max_minutes, "AA", opened_valves_setup)


def solution(filename: str) -> int:
    valves: Dict[Valve] = parse(filename)
    memo: Dict = {}
    return solve(valves, set(), memo, 30)


if __name__ == "__main__":
    print(solution("../example.txt"))
    print(solution("../input.txt"))
