import re
from enum import Enum, auto
from typing import Dict, List

# Commands
class Command(Enum):
    CD = auto()
    LS = auto()
    FILE = auto()
    DIR = auto()


class Dir:
    def __init__(self, name: str, parent) -> None:
        self.name: str = name
        self.parent: Dir = parent
        self.size = 0
        self.dirs: Dict = {}
        self.files: Dict = {}

    def add_file(self, file) -> None:
        self.files[file.name] = file

    def add_dir(self, dir) -> None:
        self.dirs[dir.name] = dir


class File:
    def __init__(self, name: str, size: str, parent: Dir) -> None:
        self.name: str = name
        self.size: int = int(size)
        self.parent: Dir = parent


def parse(terminal_output: str) -> tuple:
    commands = terminal_output.splitlines()
    for command in commands:
        # print(f"{command = }")
        if command.startswith("$ cd /"):
            yield Command.CD, "/"

        elif command.startswith("$ cd .."):
            yield Command.CD, ".."

        elif command.startswith("$ cd"):
            command_data = re.match("\$ cd (\w+)", command)
            yield Command.CD, command_data.group(1)

        elif command.startswith("$ ls"):
            continue

        elif command.startswith("dir"):
            command_data = re.match("dir (\w+)", command)
            yield Command.DIR, command_data.group(1)

        else:  # file
            command_data = re.match("(\d+) (.*)$", command)
            yield Command.FILE, (command_data.group(1), command_data.group(2))


def calculate_size(node: Dir) -> int:
    if node is None:
        return 0
    # print(node.name)
    if isinstance(node, File):
        return node.size

    total_size: int = 0
    for filename, file in node.files.items():
        total_size += calculate_size(file)
    for dirname, dir in node.dirs.items():
        total_size += calculate_size(dir)

    node.size = total_size
    # print(f"{node.name = } {node.size}")
    return total_size


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
    # file system setup
    file_system = Dir("file_system", None)
    root = Dir("/", file_system)
    file_system.add_dir(root)

    with open(filename, "r") as fp:
        terminal_output: str = fp.read()

    current = file_system
    for command, param in parse(terminal_output):
        # print(f"{command = } {param = }")
        if command == Command.CD:
            if param == "..":
                current = current.parent
            else:
                current = current.dirs[param]

        elif command == Command.FILE:
            size, name = param
            file = File(name, size, current)
            current.add_file(file)

        elif command == Command.DIR:
            dir = Dir(param, current)
            current.add_dir(dir)

    calculate_size(root)
    sum_sizes: List[int] = [0]
    get_sum_sizes(root, 100_000, sum_sizes)
    return sum_sizes[0]


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 95437

    result = solution("./input.txt")
    print(result)
