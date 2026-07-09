from typing import Dict


def parse(filename: str) -> str:
    with open(filename, "r") as fp:
        datastream: str = fp.read().strip()
    return datastream


def solve(datastream: str, target_packet_size: int) -> int:
    start: int = 0
    current: int = 0
    current_packet_size: int = 0
    seen_at: Dict[str, int] = {}

    while current < len(datastream) and current_packet_size < target_packet_size:
        char: str = datastream[current]

        if char in seen_at:
            # re setting start position and cleaning seen_at's
            new_start: int = seen_at[char] + 1
            for i in range(start, new_start):
                del seen_at[datastream[i]]
            start = new_start
            current_packet_size = current - start

        current_packet_size += 1
        seen_at[char] = current

        current += 1

    return current


def solution(filename: str, target_packet_size: int) -> int:
    datastream: str = parse(filename)
    return solve(datastream, target_packet_size)


if __name__ == "__main__":
    print(solution("./input.txt", 4))  # 1912
