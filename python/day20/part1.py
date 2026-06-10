from typing import List, Dict


class Node:
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.next: "Node" = None
        self.prev: "Node" = None

    def __repr__(self) -> str:
        return f"{self.value}"


def parse(filename: str):
    with open(filename, "r") as fp:
        str_coordinates: List = fp.read().splitlines()

    coordinates: List[Node] = [Node(int(n)) for n in str_coordinates]

    zero: Node = None
    for index, node in enumerate(coordinates):
        node.next = coordinates[(index + 1) % len(coordinates)]
        node.prev = coordinates[index - 1]
        if node.value == 0:
            zero = node

    return zero, coordinates


def solve(zero: Node, coordinates: List[Node]) -> int:

    print("Initial arrangement:")
    head: Node = coordinates[0]
    for _ in range(len(coordinates)):
        print(head, end=", ")
        head = head.next
    print("\n")

    for node in coordinates:
        # if node == zero:
        if node.value == 0:
            print("0 does not move:")
            head: Node = coordinates[0]
            for _ in range(len(coordinates)):
                print(head, end=", ")
                head = head.next
            print("\n")

            continue

        p: Node = node
        if p.value > 0:
            for _ in range(node.value):
                p = p.next
            print(f"{node.value} moves between {p.value} and {p.next.value}:")

            # if p == node or p.next == node or p.prev == node:
            #     print(f"it could be something {node}")

            # detach node
            node.prev.next = node.next
            node.next.prev = node.prev

            # DEBUG
            node.next = None
            node.prev = None

            # attach node to new position: after p
            next_: Node = p.next
            p.next = node
            next_.prev = node
            node.prev = p
            node.next = next_
        else:
            for _ in range(abs(node.value)):
                p = p.prev
            print(f"{node.value} moves between {p.prev.value} and {p.value}:")

            # if p == node or p.next == node or p.prev == node:
            #     print(f"it could be something {node}")

            # detach node
            node.prev.next = node.next
            node.next.prev = node.prev
            # attach node to new position: after p.prev
            p = p.prev

            next_: Node = p.next
            p.next = node
            next_.prev = node
            node.prev = p
            node.next = next_

            # attach node to new position: previous p
            # prev: Node = p.prev
            # p.prev = node
            # prev.next = node
            # node.next = p
            # node.prev = prev

        head: Node = coordinates[0]
        for _ in range(len(coordinates)):
            print(head, end=", ")
            head = head.next
        print("\n")

    # print(f"{len(coordinates) = }")

    # for node in coordinates:
    #     if node is None or node.next == node or node.prev == node or node.value == 0:
    #         print("got you!")

    # seen: Dict[Node] = {}
    # for node in coordinates:
    #     if id(node) in seen:
    #         print("somethings wrong")
    #         break
    #     seen[id(node)] = True
    # print(f"seen nodes {len(seen)}")

    values = [get_position(zero, place) for place in [1000, 2000, 3000]]
    print(values)
    return sum(values)


def get_position(head: Node, position: int) -> Node:
    p: Node = head
    for _ in range(position):
        p = p.next
    return p.value


def solution(filename: str) -> int:
    zero, coordinates = parse(filename)

    # seen: Dict[Node] = {}
    # for node in coordinates:
    #     if id(node) in seen:
    #         print("somethings wrong")
    #         break
    #     seen[id(node)] = True

    return solve(zero, coordinates)


if __name__ == "__main__":
    print(solution("./example.txt"))  # it should be 3
    # print(solution("./input.txt"))
