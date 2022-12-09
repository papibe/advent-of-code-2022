from typing import Dict
from part1 import solution

if __name__ == "__main__":
    result: int = solution("./data/example1.txt", 14)
    print(result)  # it should be 19

    result: int = solution("./data/example2.txt", 14)
    print(result)  # it should be 23

    result: int = solution("./data/example3.txt", 14)
    print(result)  # it should be 23

    result: int = solution("./data/example4.txt", 14)
    print(result)  # it should be 29

    result: int = solution("./data/example5.txt", 14)
    print(result)  # it should be 26

    result: int = solution("./data/input.txt", 14)
    print(result)
