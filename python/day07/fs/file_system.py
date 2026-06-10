import re
from enum import Enum, auto
from typing import Dict, List


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


def calculate_dir_sizes(node: Dir) -> int:
    if node is None:
        return 0
    if isinstance(node, File):
        return node.size

    total_size: int = 0
    for filename, file in node.files.items():
        total_size += calculate_dir_sizes(file)
    for dirname, dir in node.dirs.items():
        total_size += calculate_dir_sizes(dir)

    node.size = total_size
    return total_size


def create_filesystem_tree(terminal_output: str) -> Dir:
    # file system setup. Use a dummy root node
    file_system = Dir("file_system", None)
    root = Dir("/", file_system)
    file_system.add_dir(root)

    current = file_system
    for command, param in parse(terminal_output):
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

    return root
