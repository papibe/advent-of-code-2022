import re
from enum import Enum, auto
from typing import Dict, Generator, List, Optional, Tuple


class Command(Enum):
    CD = auto()
    LS = auto()
    FILE = auto()
    DIR = auto()


class Dir:
    def __init__(self, name: str, parent: Optional["Dir"]) -> None:
        self.name: str = name
        self.parent: Optional[Dir] = parent
        self.size = 0
        self.dirs: Dict[str, Dir] = {}
        self.files: Dict[str, File] = {}

    def add_file(self, file: "File") -> None:
        self.files[file.name] = file

    def add_dir(self, dir: "Dir") -> None:
        self.dirs[dir.name] = dir

    def update_dir_sizes(self) -> None:
        def dfs(node: Dir) -> int:
            total_size: int = 0
            for _, file in node.files.items():
                total_size += file.size

            for _, dir in node.dirs.items():
                total_size += dfs(dir)

            node.size = total_size
            return total_size

        _ = dfs(self)


class File:
    def __init__(self, name: str, size: str, parent: Dir) -> None:
        self.name: str = name
        self.size: int = int(size)
        self.parent: Dir = parent


def parse(terminal_output: str) -> Generator[Tuple[Command, str], None, None]:
    commands: List[str] = terminal_output.splitlines()

    for command in commands:
        if command.startswith("$ cd /"):
            yield Command.CD, "/"

        elif command.startswith("$ cd .."):
            yield Command.CD, ".."

        elif command.startswith("$ cd"):
            command_data = re.match(r"\$ cd (\w+)", command)
            if command_data:
                yield Command.CD, command_data.group(1)

        elif command.startswith("$ ls"):
            continue

        elif command.startswith("dir"):
            command_data = re.match(r"dir (\w+)", command)
            if command_data:
                yield Command.DIR, command_data.group(1)

        else:  # file
            command_data = re.match(r"(\d+) (.*)$", command)
            if command_data:
                yield Command.FILE, command_data.group(0)


def create_filesystem_tree(terminal_output: str) -> Dir:
    # file system setup. Use a dummy root node
    file_system: Dir = Dir("file_system", None)
    root: Dir = Dir("/", file_system)
    file_system.add_dir(root)

    current: Dir = file_system
    for command, param in parse(terminal_output):
        if command == Command.CD:
            if param == "..":
                if current.parent:
                    current = current.parent
            else:
                current = current.dirs[param]

        elif command == Command.FILE:
            size, name = param.split()
            file: File = File(name, size, current)
            current.add_file(file)

        elif command == Command.DIR:
            subdir: Dir = Dir(param, current)
            current.add_dir(subdir)

    return root
