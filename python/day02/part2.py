from collections import namedtuple
from typing import Dict, List

Play = namedtuple("Play", ["their_play", "my_strategy"])

ROCK: str = "A"
PAPER: str = "B"
SCISSORS: str = "C"

# strategy translation
LOSE: str = "X"
DRAW: str = "Y"
WIN: str = "Z"

choice: Dict[str, Dict[str, str]] = {
    LOSE: {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER},
    DRAW: {ROCK: ROCK, PAPER: PAPER, SCISSORS: SCISSORS},
    WIN: {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK},
}

play_value: Dict[str, int] = {ROCK: 1, PAPER: 2, SCISSORS: 3}

match_result_value: Dict[str, Dict[str, int]] = {
    ROCK: {ROCK: 3, PAPER: 6, SCISSORS: 0},
    PAPER: {ROCK: 0, PAPER: 3, SCISSORS: 6},
    SCISSORS: {ROCK: 6, PAPER: 0, SCISSORS: 3},
}


def parse(filename: str) -> List[Play]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    plays: List[Play] = []
    for line in data:
        line_split: List[str] = line.split()
        their_play: str = line_split[0]
        my_strategy: str = line_split[1]
        plays.append(Play(their_play, my_strategy))

    return plays


def solve(plays: List[Play]) -> int:
    points: int = 0
    for play in plays:
        my_play = choice[play.my_strategy][play.their_play]
        points += play_value[my_play] + match_result_value[play.their_play][my_play]

    return points


def solution(filename: str) -> int:
    plays: List[Play] = parse(filename)
    return solve(plays)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 12
    print(solution("./input.txt"))  # 13693
