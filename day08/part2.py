from typing import List


class Tree:
    def __init__(self, height: int) -> None:
        self.height = int(height)
        self.visible = False

    def set_visible(self, visibility: bool) -> None:
        self.visible = visibility

    def is_visible(self) -> bool:
        return self.visible


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read()

    trees: List[List[str]] = [list(map(Tree, row)) for row in data.splitlines()]
    trees_size: int = len(trees)

    scenic_score: int = 0
    for row in range(1, trees_size - 1):
        for col in range(1, trees_size - 1):
            height: int = trees[row][col].height
            # up
            scenic_score_up: int = 0
            for lrow in range(row - 1, -1, -1):
                if trees[lrow][col].height >= height:
                    scenic_score_up += 1
                    break
                if trees[lrow][col].height < height:
                    scenic_score_up += 1
            # right
            scenic_score_right: int = 0
            for lcol in range(col + 1, trees_size):
                if trees[row][lcol].height >= height:
                    scenic_score_right += 1
                    break
                if trees[row][lcol].height < height:
                    scenic_score_right += 1
            # down
            scenic_score_down: int = 0
            for lrow in range(row + 1, trees_size):
                if trees[lrow][col].height >= height:
                    scenic_score_down += 1
                    break
                if trees[lrow][col].height < height:
                    scenic_score_down += 1
            # left
            scenic_score_left: int = 0
            for lcol in range(col - 1, -1, -1):
                if trees[row][lcol].height >= height:
                    scenic_score_left += 1
                    break
                if trees[row][lcol].height < height:
                    scenic_score_left += 1

            scenic_score = max(
                scenic_score,
                scenic_score_up
                * scenic_score_right
                * scenic_score_down
                * scenic_score_left,
            )

    return scenic_score


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)

    result = solution("./input.txt")
    print(result)
