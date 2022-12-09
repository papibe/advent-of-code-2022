from typing import List

ROCK, PAPER, SCISSORS = "A", "B", "C"

# strategy translation
LOSE, DRAW, WIN = "X", "Y", "Z"
choice = {
    LOSE: {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER},
    DRAW: {ROCK: ROCK, PAPER: PAPER, SCISSORS: SCISSORS},
    WIN: {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK},
}

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
        my_play = choice[my_strategy][other_play]
        points += play_value[my_play] + match_result_value[other_play][my_play]

    return points


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 15

    result: int = solution("./input.txt")
    print(result)
