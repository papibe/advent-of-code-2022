from typing import List, Dict


class Node:
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.next: "Node" = None
        self.prev: "Node" = None

    def __repr__(self) -> str:
        return f"{self.value}"


def parse(filename: str, decription_key: int):
    with open(filename, "r") as fp:
        str_coordinates: List = fp.read().splitlines()

    coordinates: List[Node] = [Node(int(n) * decription_key) for n in str_coordinates]
    # coordinates: List[Node] = [Node(int(n)) for n in str_coordinates]

    zero: Node = None
    for index, node in enumerate(coordinates):
        node.next = coordinates[(index + 1) % len(coordinates)]
        node.prev = coordinates[index - 1]
        if node.value == 0:
            zero = node

    return zero, coordinates


def solve(zero: Node, coordinates: List[Node]) -> int:

    # print("Initial arrangement:")
    # head: Node = zero
    # for _ in range(len(coordinates)):
    #     print(head, end=", ")
    #     head = head.next
    # print("\n")

    for node in coordinates:
        if node == zero:
            # if node.value == 0:
            # print("0 does not move:")
            # head: Node = coordinates[0]
            # for _ in range(len(coordinates)):
            #     print(head, end=", ")
            #     head = head.next
            # print("\n")

            continue

        # p: Node = node
        # if p.value > 0:
        #     cycle: int = node.value % len(coordinates)
        # else:
        #     cycle = (node.value % -len(coordinates)) + len(coordinates) - 1
        #     print(f"{node.value} -> {cycle}")

        if node.value > 0:
            # if node.value >= len(coordinates):
            #     # cycle: int = node.value % len(coordinates) + 1
            #     cycle: int = node.value % len(coordinates) + 1
            # else:
            #     cycle: int = node.value

            # for _ in range(cycle):
            # for _ in range(node.value % len(coordinates)):
            # for _ in range(node.value):
            for _ in range(node.value % (len(coordinates) - 1)):
                previous_node: Node = node.prev
                next_node: Node = node.next
                forward_node: Node = next_node.next

                previous_node.next = next_node

                next_node.next = node
                next_node.prev = previous_node

                node.prev = next_node
                node.next = forward_node

                forward_node.prev = node

            # print(f"{node} moves between {next_node} and {forward_node}:")
            # break

        else:
            # if node.value <= -len(coordinates):
            #     # cycle: int = ((node.value) % -len(coordinates)) - 1
            #     cycle: int = ((node.value) % -len(coordinates))
            # else:
            #     cycle: int = node.value

            # for _ in range(abs(node.value)):
            # for _ in range(abs(cycle)):
            for _ in range(abs(node.value % -(len(coordinates) - 1))):

            # for _ in range(abs(node.value)):
                next_node: Node = node.next
                previous_node: Node = node.prev
                back_node: Node = previous_node.prev

                back_node.next = node

                node.prev = back_node
                node.next = previous_node

                previous_node.prev = node
                previous_node.next = next_node

                next_node.prev = previous_node

            # print(f"{node} moves between {back_node} and {previous_node}:")
            # break
        # head: Node = coordinates[0]
        # for _ in range(len(coordinates)):
        #     print(head, end=", ")
        #     head = head.next
        # print("\n")

    # head: Node = zero
    # for _ in range(len(coordinates)):
    #     print(head, end=", ")
    #     head = head.next
    # print("\n")

    values = [get_position(zero, place) for place in [1000, 2000, 3000]]
    # print(values)
    return sum(values)


def get_position(head: Node, position: int) -> Node:
    p: Node = head
    for _ in range(position):
        p = p.next
    return p.value


def solution(filename: str, decryption_key: int) -> int:
    zero, coordinates = parse(filename, decryption_key)

    for _ in range(10):
        result = solve(zero, coordinates)

    return result

if __name__ == "__main__":
    # print(solution("./example.txt", 811589153))  # it should be 3
    print(solution("./input.txt", 811589153))
