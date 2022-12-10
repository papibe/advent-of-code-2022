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

    # top row
    for col in range(trees_size):
        trees[0][col].set_visible(True)
        max_tree: int = trees[0][col].height

        for row in range(1, trees_size):
            current_tree: Tree = trees[row][col]
            if current_tree.height > max_tree:
                current_tree.set_visible(True)
                max_tree = max(max_tree, current_tree.height)

    # right col
    for row in range(trees_size):
        trees[row][trees_size - 1].set_visible(True)
        max_tree: int = trees[row][trees_size - 1].height

        for col in range(trees_size - 2, -1, -1):
            current_tree: Tree = trees[row][col]
            if current_tree.height > max_tree:
                current_tree.set_visible(True)
                max_tree = max(max_tree, current_tree.height)

    # bottom row
    for col in range(trees_size):
        trees[trees_size - 1][col].set_visible(True)
        max_tree: int = trees[trees_size - 1][col].height

        for row in range(trees_size - 2, -1, -1):
            current_tree: Tree = trees[row][col]
            if current_tree.height > max_tree:
                current_tree.set_visible(True)
                max_tree = max(max_tree, current_tree.height)

    # left col
    for row in range(trees_size):
        trees[row][0].set_visible(True)
        max_tree: int = trees[row][0].height

        for col in range(1, trees_size - 1):
            current_tree: Tree = trees[row][col]
            if current_tree.height > max_tree:
                current_tree.set_visible(True)
                max_tree = max(max_tree, current_tree.height)

    # count visible trees:
    visible_trees: int = 0
    for row in trees:
        for tree in row:
            if tree.is_visible():
                visible_trees += 1
    return visible_trees


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)

    result = solution("./input.txt")
    print(result)
