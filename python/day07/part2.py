from fs.file_system import Dir, create_filesystem_tree


def parse(filename: str) -> str:
    with open(filename, "r") as fp:
        terminal_output: str = fp.read()
    return terminal_output


def get_min_directory(node: Dir, space_left: int, space_needed: int) -> int:
    min_size: int = float("inf")  # type: ignore

    def dfs(node: Dir) -> None:
        nonlocal min_size

        if node.size + space_left >= space_needed:
            min_size = min(min_size, node.size)

        for _, subdir in node.dirs.items():
            dfs(subdir)

    dfs(node)
    return min_size


def solution(filename: str) -> int:
    terminal_output: str = parse(filename)

    root = create_filesystem_tree(terminal_output)
    root.update_dir_sizes()

    space_left = 70_000_000 - root.size

    return get_min_directory(root, space_left, 30_000_000)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 24933642
    print(solution("./input.txt"))  # 5883165
