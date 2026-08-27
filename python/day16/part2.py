import re
from typing import Dict, List, Match, Optional, Tuple

type AdjacencyMatrix = List[List[int]]
type ValveIndex = Dict[str, int]
type Flows = Dict[str, int]
type State = Tuple[int, int, int]


def parse(filename: str) -> Tuple[AdjacencyMatrix, ValveIndex, Flows]:
    with open(filename, "r") as file:
        data: List[str] = file.read().splitlines()

    re_fmt: str = r"Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
    flows: Dict[str, int] = {}
    tunnels: Dict[str, List[str]] = {}

    for line in data:
        re_parsed: Optional[Match[str]] = re.match(re_fmt, line)
        if re_parsed:
            valve: str = re_parsed.group(1)
            flow: int = int(re_parsed.group(2))
            valves: List[str] = [v.strip() for v in re_parsed.group(3).split(",")]
            flows[valve] = flow
            tunnels[valve] = valves

    adjacency_matrix: AdjacencyMatrix = [
        [float("inf")] * len(data) for _ in range(len(data))  # type: ignore
    ]

    valve_index: Dict[str, int] = {key: index for index, key in enumerate(flows.keys())}
    for valve, neighbors in tunnels.items():
        for nb in neighbors:
            adjacency_matrix[valve_index[valve]][valve_index[nb]] = 1
            adjacency_matrix[valve_index[valve]][valve_index[valve]] = 0

    return adjacency_matrix, valve_index, flows


def floyd_warshall(adjacency_matrix: AdjacencyMatrix) -> None:
    n: int = len(adjacency_matrix)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                # if dp[i][k] + dp[k][j] < dp[i][j]:
                #     dp[i][j] = dp[i][k] + dp[k][j]
                adjacency_matrix[i][j] = min(
                    adjacency_matrix[i][j],
                    adjacency_matrix[i][k] + adjacency_matrix[k][j],
                )


def trim_valves(
    am: AdjacencyMatrix,
    valve_index: Dict[str, int],
    flows: Dict[str, int],
) -> Tuple[List[List[int]], Dict[str, int], Dict[str, int]]:

    valves_with_flow: Dict[str, int] = {
        valve: flow for valve, flow in flows.items() if flow > 0
    }
    valves_with_flow["AA"] = 0
    new_valve_index: Dict[str, int] = {
        key: index for index, key in enumerate(valves_with_flow.keys())
    }

    n: int = len(valves_with_flow)
    adjacency_matrix: List[List[int]] = [[float("inf")] * n for _ in range(n)]  # type: ignore

    for valve in valves_with_flow:
        for connecting_valve in valves_with_flow:
            adjacency_matrix[new_valve_index[valve]][
                new_valve_index[connecting_valve]
            ] = am[valve_index[valve]][valve_index[connecting_valve]]

    return adjacency_matrix, new_valve_index, valves_with_flow


def solve(
    am: AdjacencyMatrix,
    flows: List[int],
    valve_index: ValveIndex,
    opened_valves: int,
    memo: Dict[State, int],
    max_minutes: int,
) -> int:
    def sol(minutes: int, valve: int, opened: int) -> int:
        if minutes == 0:
            return 0

        if (minutes, valve, opened) in memo:
            return memo[(minutes, valve, opened)]

        max_pressure: int = 0
        for neighbor, distance in enumerate(am[valve]):
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

    return sol(max_minutes, valve_index["AA"], opened_valves | (1 << valve_index["AA"]))


def solution(filename: str) -> int:
    adjacency_matrix: AdjacencyMatrix
    valve_index: ValveIndex
    flows: Flows
    adjacency_matrix, valve_index, flows = parse(filename)

    floyd_warshall(adjacency_matrix)
    adjacency_matrix, new_valve_index, valves_with_flow = trim_valves(
        adjacency_matrix, valve_index, flows
    )
    memo: Dict[State, int] = {}
    new_flows: List[int] = list(valves_with_flow.values())

    max_team_pressure: int = 0
    times: int = (1 << len(new_flows)) - 1
    for bitmask in range(times // 2):
        max_team_pressure = max(
            max_team_pressure,
            solve(adjacency_matrix, new_flows, new_valve_index, bitmask, memo, 26)
            + solve(
                adjacency_matrix, new_flows, new_valve_index, bitmask ^ times, memo, 26
            ),
        )

    return max_team_pressure


if __name__ == "__main__":
    print(solution("./example.txt"))  # 1707
    print(solution("./input.txt"))  # 2520
