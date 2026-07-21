from typing import List

Trees = List[List[int]]


def parse(filename: str) -> Trees:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    return [[int(tree) for tree in row] for row in data]


def solve(trees: Trees) -> int:
    size: int = len(trees)

    max_scenic_score: int = 0
    for current_row in range(1, size - 1):
        for current_col in range(1, size - 1):
            height: int = trees[current_row][current_col]
            # up
            current_ss_up: int = 0
            for row in range(current_row - 1, -1, -1):
                current_ss_up += 1
                if trees[row][current_col] >= height:
                    break
            # right
            current_ss_right: int = 0
            for col in range(current_col + 1, size):
                current_ss_right += 1
                if trees[current_row][col] >= height:
                    break
            # down
            current_ss_down: int = 0
            for row in range(current_row + 1, size):
                current_ss_down += 1
                if trees[row][current_col] >= height:
                    break
            # left
            current_ss_left: int = 0
            for col in range(current_col - 1, -1, -1):
                current_ss_left += 1
                if trees[current_row][col] >= height:
                    break

            current_score: int = (
                current_ss_up * current_ss_right * current_ss_down * current_ss_left
            )
            max_scenic_score = max(max_scenic_score, current_score)

    return max_scenic_score


def solution(filename: str) -> int:
    trees: Trees = parse(filename)
    return solve(trees)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 8
    print(solution("./input.txt"))  # 263670
