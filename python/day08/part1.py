from typing import List, Set, Tuple

Trees = List[List[int]]


def parse(filename: str) -> Trees:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    return [[int(tree) for tree in row] for row in data]


def solve(trees: Trees) -> int:
    size: int = len(trees)
    visible_trees: Set[Tuple[int, int]] = set()

    # top row
    for col in range(size):
        max_tree: int = trees[0][col]
        visible_trees.add((0, col))

        for row in range(size):
            if trees[row][col] > max_tree:
                visible_trees.add((row, col))
                max_tree = max(max_tree, trees[row][col])

    # right col
    for row in range(size):
        max_tree = trees[row][size - 1]
        visible_trees.add((row, size - 1))

        for col in range(size - 1, -1, -1):
            if trees[row][col] > max_tree:
                visible_trees.add((row, col))
                max_tree = max(max_tree, trees[row][col])

    # bottom row
    for col in range(size):
        max_tree = trees[size - 1][col]
        visible_trees.add((size - 1, col))

        for row in range(size - 1, -1, -1):
            if trees[row][col] > max_tree:
                visible_trees.add((row, col))
                max_tree = max(max_tree, trees[row][col])

    # left col
    for row in range(size):
        max_tree = trees[row][0]
        visible_trees.add((row, 0))

        for col in range(size):
            if trees[row][col] > max_tree:
                visible_trees.add((row, col))
                max_tree = max(max_tree, trees[row][col])

    return len(visible_trees)


def solution(filename: str) -> int:
    trees: Trees = parse(filename)
    return solve(trees)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 21
    print(solution("./input.txt"))  # 1835
