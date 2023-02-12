import re
from enum import Enum, auto
from typing import List, Dict


class NodeType(Enum):
    value: str = auto()
    operation: str = auto()


class TreeNode:
    def __init__(
        self,
        monkey_name: str,
        value: int = None,
        monkey_oper1: str = None,
        operation: str = None,
        monkey_oper2: str = None,
    ) -> None:
        self.monkey_name: str = monkey_name
        self.value: int = value
        self.monkey_oper1: str = monkey_oper1
        self.operation: str = operation
        self.monkey_oper2: str = monkey_oper2

        self.type: NodeType = (
            NodeType.value if value is not None else NodeType.operation
        )

        self.left_child: "TreeNode" = None
        self.right_child: "TreeNode" = None


def parse(filename: str) -> Dict[str, TreeNode]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    monkey_registry: Dict[str, TreeNode] = {}

    number_re: str = r"(\w+): (\d+)"
    math_re: str = r"(\w+): (\w+) ([\+\-\*/]) (\w+)"

    for line in data:
        match_number_expr = re.match(number_re, line)
        match_math_expr = re.match(math_re, line)

        if match_number_expr:
            monkey_name: str = match_number_expr.group(1)
            yelled_value: int = int(match_number_expr.group(2))
            node: TreeNode = TreeNode(monkey_name=monkey_name, value=yelled_value)
            # print("number line:\t", line)

        if match_math_expr:
            monkey_name: str = match_math_expr.group(1)
            monkey_oper1: str = match_math_expr.group(2)
            operation: str = match_math_expr.group(3)
            monkey_oper2: str = match_math_expr.group(4)
            node: TreeNode = TreeNode(
                monkey_name=monkey_name,
                monkey_oper1=monkey_oper1,
                operation=operation,
                monkey_oper2=monkey_oper2,
            )
            # print("math operation:\t", line)

        monkey_registry[monkey_name] = node

    return monkey_registry


def form_expression_tree(
    monkey_registry: Dict[str, TreeNode], monkey_name: str
) -> TreeNode:
    node: TreeNode = monkey_registry[monkey_name]
    if node.type == NodeType.operation:
        node.left_child = form_expression_tree(monkey_registry, node.monkey_oper1)
        node.right_child = form_expression_tree(monkey_registry, node.monkey_oper2)
    return node


def eval_tree(node: TreeNode) -> int:
    if node.type == NodeType.value:
        return node.value

    left_value: int = eval_tree(node.left_child)
    right_value: int = eval_tree(node.right_child)

    if node.operation == "+":
        return left_value + right_value
    if node.operation == "-":
        return left_value - right_value
    if node.operation == "*":
        return left_value * right_value
    if node.operation == "/":
        return left_value // right_value  # regular '/' works too


def solution(filename: str):
    monkey_registry: Dict[TreeNode] = parse(filename)
    tree: TreeNode = form_expression_tree(monkey_registry, "root")

    return eval_tree(tree)


if __name__ == "__main__":
    print(solution("./example.txt"))
    print(solution("./input.txt"))