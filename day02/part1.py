from typing import List

ROCK, PAPER, SCISSORS = "A", "B", "C"

# strategy translation
strategy = {"X": ROCK, "Y": PAPER, "Z": SCISSORS}

play_value = {ROCK: 1, PAPER: 2, SCISSORS: 3}

match_result_value = {
    ROCK: {ROCK: 3, PAPER: 6, SCISSORS: 0},
    PAPER: {ROCK: 0, PAPER: 3, SCISSORS: 6},
    SCISSORS: {ROCK: 6, PAPER: 0, SCISSORS: 3},
}


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        plays: List[str] = fp.read().splitlines()

    points: int = 0
    for play in plays:
        other_play, my_strategy = play.split()
        my_play = strategy[my_strategy]
        points += play_value[my_play] + match_result_value[other_play][my_play]

    return points


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 12

    result: int = solution("./input.txt")
    print(result)
