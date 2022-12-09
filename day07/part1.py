from typing import List

from fs.file_system import Dir, File, create_filesystem_tree, calculate_dir_sizes


def get_sum_sizes(node: Dir, max_size: int, value: List[int]) -> None:
    if node is None:
        return 0
    if isinstance(node, File):
        return 0
    if node.size <= max_size:
        value[0] += node.size
    for dirname, dir in node.dirs.items():
        get_sum_sizes(dir, max_size, value)


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        terminal_output: str = fp.read()

    root = create_filesystem_tree(terminal_output)
    calculate_dir_sizes(root)

    sum_sizes: List[int] = [0]
    get_sum_sizes(root, 100_000, sum_sizes)

    return sum_sizes[0]


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 95437

    result = solution("./input.txt")
    print(result)
