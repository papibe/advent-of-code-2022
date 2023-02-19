import re
from typing import List, Dict, Tuple
from copy import deepcopy


def parse(filename: str) -> Tuple[List, Dict]:
    with open(filename, "r") as file:
        data = file.read().splitlines()

    re_fmt: str = r"Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
    flows: Dict[str, int] = {}
    tunnels: Dict[str, List[str]] = {}

    for line in data:
        re_parsed = re.match(re_fmt, line)
        valve: str = re_parsed.group(1)
        flow: int = int(re_parsed.group(2))
        valves: List[str] = [v.strip() for v in re_parsed.group(3).split(",")]
        flows[valve] = flow
        tunnels[valve] = valves

    adjacency_matrix: List[List[int]] = [
        [float("inf")] * len(data) for _ in range(len(data))
    ]

    valve_index = {key: index for index, key in enumerate(flows.keys())}
    for valve, neighbors in tunnels.items():
        for nb in neighbors:
            adjacency_matrix[valve_index[valve]][valve_index[nb]] = 1
            adjacency_matrix[valve_index[valve]][valve_index[valve]] = 0

    return adjacency_matrix, valve_index, flows


def floyd_warshall(adjacency_matrix):
    dp = deepcopy(adjacency_matrix)
    n = len(adjacency_matrix)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                # if dp[i][k] + dp[k][j] < dp[i][j]:
                #     dp[i][j] = dp[i][k] + dp[k][j]
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])
    return dp


def trim_valves(dp, valve_index, flows):
    valves_with_flow = {valve: flow for valve, flow in flows.items() if flow > 0}
    valves_with_flow["AA"] = 0
    new_valve_index = {key: index for index, key in enumerate(valves_with_flow.keys())}

    adjacency_matrix: List[List[int]] = [
        [float("inf")] * len(valves_with_flow) for _ in range(len(valves_with_flow))
    ]

    for valve in valves_with_flow:
        for connecting_valve in valves_with_flow:
            adjacency_matrix[new_valve_index[valve]][
                new_valve_index[connecting_valve]
            ] = dp[valve_index[valve]][valve_index[connecting_valve]]

    return adjacency_matrix, new_valve_index, valves_with_flow


def solve(
    am: List[List[int]],
    flows: List[int],
    valve_index: Dict[str, int],
    opened_valves: int,
    memo: Dict,
    max_minutes: int,
) -> int:
    def sol(minutes: int, valve: str, opened: int):
        if minutes == 0:
            return 0

        if (minutes, valve, opened) in memo:
            return memo[(minutes, valve, opened)]

        max_pressure: int = 0
        for neighbor, distance in enumerate(am[valve]):
            if neighbor == valve:
                continue
            if distance <= minutes - 1:
                neighbor_bit = 1 << neighbor
                if opened & neighbor_bit == 0:  # not opened
                    max_pressure = max(
                        max_pressure,
                        flows[neighbor] * (minutes - distance - 1)
                        + sol(minutes - distance - 1, neighbor, opened | neighbor_bit),
                    )

        memo[(minutes, valve, opened)] = max_pressure
        return max_pressure

    return sol(max_minutes, valve_index["AA"], opened_valves << valve_index["AA"])


def solution(filename: str) -> int:
    adjacency_matrix, valve_index, flows = parse(filename)
    dp = floyd_warshall(adjacency_matrix)
    adjacency_matrix, new_valve_index, valves_with_flow = trim_valves(
        dp, valve_index, flows
    )
    memo: Dict = {}
    new_flows = list(valves_with_flow.values())

    return solve(adjacency_matrix, new_flows, new_valve_index, 0, memo, 30)


if __name__ == "__main__":
    print(solution("../example.txt"))
    print(solution("../input.txt"))
