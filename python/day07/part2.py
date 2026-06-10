from typing import List

from fs.file_system import Dir, File, create_filesystem_tree, calculate_dir_sizes


def get_min_directory(
    node: Dir, space_left: int, space_needed: int, min_size: List[int]
) -> None:
    if node is None or isinstance(node, File):
        return
    if node.size + space_left >= space_needed:
        min_size[0] = min(min_size[0], node.size)
    for dirname, dir in node.dirs.items():
        get_min_directory(dir, space_left, space_needed, min_size)


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        terminal_output: str = fp.read()

    root = create_filesystem_tree(terminal_output)
    calculate_dir_sizes(root)

    space_left = 70_000_000 - root.size
    min_size: List[int] = [float("inf")]
    get_min_directory(root, space_left, 30_000_000, min_size)

    return min_size[0]


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 95437

    result = solution("./input.txt")
    print(result)
