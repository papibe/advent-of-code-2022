from fs.file_system import Dir, create_filesystem_tree


def parse(filename: str) -> str:
    with open(filename, "r") as fp:
        terminal_output: str = fp.read()
    return terminal_output


def get_sum_sizes(node: Dir, max_size: int) -> int:
    total_sum: int = 0

    def dfs(node: Dir) -> None:
        nonlocal total_sum

        if node.size <= max_size:
            total_sum += node.size

        for _, subdir in node.dirs.items():
            dfs(subdir)

    dfs(node)
    return total_sum


def solution(filename: str) -> int:
    terminal_output: str = parse(filename)

    root = create_filesystem_tree(terminal_output)
    root.update_dir_sizes()

    return get_sum_sizes(root, 100_000)


if __name__ == "__main__":
    print(solution("./example.txt"))  #  95437
    print(solution("./input.txt"))  #  2104783
