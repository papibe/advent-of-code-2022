from typing import Dict


def solution(filename: str, packet_size: int) -> str:
    with open(filename, "r") as fp:
        datastream: str = fp.read()

    start: int = 0
    current: int = -1
    seen_char: Dict[str, int] = {}

    while current < len(datastream) and (current - start + 1) < packet_size:
        current += 1
        char = datastream[current]

        if char not in seen_char:
            seen_char[char] = current
        else:
            # reseting start position and cleaning seen dicts
            new_start = seen_char[char] + 1
            for i in range(start, new_start):
                del seen_char[datastream[i]]

            seen_char[char] = current
            start = new_start

    return current + 1


if __name__ == "__main__":
    result: int = solution("./data/example1.txt", 4)
    print(result)  # it should be 7

    result = solution("./data/example2.txt", 4)
    print(result)  # it should be 5

    result = solution("./data/example3.txt", 4)
    print(result)  # it should be 6

    result = solution("./data/example4.txt", 4)
    print(result)  # it should be 10

    result = solution("./data/example5.txt", 4)
    print(result)  # it should be 11

    result = solution("./data/input.txt", 4)
    print(result)
