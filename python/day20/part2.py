from typing import List, Optional, Tuple


class Node:
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.next: Optional["Node"] = None
        self.prev: Optional["Node"] = None


def parse(filename: str, decryption_key: int) -> Tuple[Node, List[Node]]:
    with open(filename, "r") as fp:
        str_coordinates: List[str] = fp.read().splitlines()

    coordinates: List[Node] = [Node(int(n) * decryption_key) for n in str_coordinates]

    zero: Optional[Node] = None
    for index, node in enumerate(coordinates):
        node.next = coordinates[(index + 1) % len(coordinates)]
        node.prev = coordinates[index - 1]
        if node.value == 0:
            zero = node

    if not zero:
        raise RuntimeError("no zero found!")

    return zero, coordinates


def get_position(head: Node, position: int) -> int:
    p: Optional[Node] = head
    for _ in range(position):
        p = p.next  # type: ignore
    return p.value  # type: ignore


def solve(zero: Node, coordinates: List[Node]) -> int:
    n: int = len(coordinates)

    for node in coordinates:
        if node == zero:
            continue

        if node.value > 0:
            iter_range = node.value % (n - 1)
        else:
            iter_range = (node.value - n + 1) % (n - 1)

        previous_node: Node = node.prev  # type: ignore
        next_node: Node = node.next  # type: ignore
        p: Node = node

        for _ in range(iter_range):
            p = p.next  # type: ignore

        # remove from original position
        previous_node.next = next_node
        next_node.prev = previous_node

        # insert in new position
        node.prev = p
        node.next = p.next

        tmp: Node = p.next  # type: ignore
        p.next = node
        tmp.prev = node

    return sum([get_position(zero, place) for place in [1000, 2000, 3000]])


def solution(filename: str, decryption_key: int) -> int:
    zero, coordinates = parse(filename, decryption_key)

    for _ in range(10):
        result = solve(zero, coordinates)

    return result


if __name__ == "__main__":
    print(solution("./example.txt", 811589153))  # 1623178306
    print(solution("./input.txt", 811589153))  # 535648840980
