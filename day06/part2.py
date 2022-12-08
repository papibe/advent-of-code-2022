from typing import Dict


def solution(filename: str) -> str:
    with open(filename, "r") as fp:
        datastream: str = fp.read()

    start: int = 0
    current: int = -1
    seen_char: Dict[str, int] = {}
    seen_pos: Dict[int, str] = {}

    while current < len(datastream) and (current - start + 1) < 14:
        current += 1
        char = datastream[current]

        if char not in seen_char:
            seen_char[char] = current
            seen_pos[current] = char
        else:
            # reseting start position and cleaning seen dicts
            new_start = seen_char[char] + 1
            for i in range(start, new_start):
                del seen_char[seen_pos[i]]
                del seen_pos[i]

            seen_char[char] = current
            seen_pos[current] = char
            start = new_start

    return current + 1


if __name__ == "__main__":
    result: int = solution("./data/example1.txt")
    print(result)  # it should be 19

    result: int = solution("./data/example2.txt")
    print(result)  # it should be 23

    result: int = solution("./data/example3.txt")
    print(result)  # it should be 23

    result: int = solution("./data/example4.txt")
    print(result)  # it should be 29

    result: int = solution("./data/example5.txt")
    print(result)  # it should be 26

    result: int = solution("./data/input.txt")
    print(result)
