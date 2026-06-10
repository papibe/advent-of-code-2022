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
    valves: Dict[str, Valve], opened_valves_setup: Set[str], max_minutes: int
) -> int:
    minute: int = 0
    queue: Deque = deque()

    max_pressure: int = 0
    history: Dict[str, int] = {valve: -1 for valve in valves}
    queue.append((minute, "AA", 0, history, opened_valves_setup))

    state: Set = set([(minute, "AA", 0)])
    history["AA"] = 0

    while queue:
        minute, valve, current_pressure, history, opened = queue.popleft()
        # new_history: Dict = history.copy()
        # new_history[valve] = max(new_history[valve], current_pressure)
        print(minute, valve, current_pressure)
        # print(new_history)
        # print()
        max_pressure = max(max_pressure, current_pressure)
        if minute > max_minutes:
            # print("reached 30!")
            # break
            print(opened)
            continue
        # max_pressure = max(max_pressure, current_pressure)

        # not open valve
        for neighbor in valves[valve].neighbors:
            if current_pressure > history[neighbor]:
                new_history: Dict = history.copy()
                new_history[neighbor] = current_pressure
                next_state: Tuple = (minute + 1, neighbor, current_pressure)
                if next_state in state:
                    # print("save")
                    pass
                else:
                    state.add(next_state)
                    queue.append(
                        (minute + 1, neighbor, current_pressure, new_history, opened)
                    )

        if valves[valve].flow > 0 and valve not in opened:
            current_pressure += valves[valve].flow * (30 - minute - 1)
            new_opened = opened.copy()
            new_opened.add(valve)

            new_history_2: Dict = history.copy()
            new_history_2[valve] = current_pressure

            next_state: Tuple = (minute + 1, valve, current_pressure)
            if next_state in state:
                print("save")
                pass
            else:
                state.add(next_state)
                queue.append(
                    (minute + 1, valve, current_pressure, new_history_2, new_opened)
                )

            # print(minute, valve, current_pressure, f"{valve} opened")

            # minute += 1  # walk to other valve
            # for neighbor in valves[valve].neighbors:
            #     if neighbor not in history or current_pressure > history[neighbor]:
            #         history[neighbor] = current_pressure
            #         queue.append((minute, neighbor, current_pressure, new_opened))

    return max_pressure


def solution(filename: str) -> int:
    valves: Dict[Valve] = parse(filename)

    # good_valves = [valve for valve in valves if valves[valve].flow > 0]

    # max_team_preassure: int = 0
    # for length in range(len(valves) + 1):
    #     for subset in itertools.combinations(good_valves, length):
    #         other_subnet = [valve for valve in good_valves if valve not in subset]
    #         player1_preassure: int = solve(valves, set(subset))
    #         player2_preassure: int = solve(valves, set(other_subnet))

    #         max_team_preassure = max(max_team_preassure, player1_preassure + player2_preassure)
    #         print(f"{player1_preassure = }, {player2_preassure = } {max_team_preassure = }")
    #         print("+" * 50)
    #         # break

    # return max_team_preassure

    return solve(valves, set(), 30)


if __name__ == "__main__":
    # result: int = solution("./example.txt")
    # print(result)

    result = solution("./input.txt")
    print(result)
