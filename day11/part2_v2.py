import re
from typing import List, Set, Tuple, Dict


class Monkey:
    def __init__(
        self,
        id: int,
        items: List[int],
        operation: str,
        test_divisible: int,
        true_monkey: int,
        false_monkey: int,
    ) -> None:
        self.id: int = id
        self.items: List[int] = items
        self.operation: str = operation
        self.test_divisible: int = test_divisible
        self.true_monkey: int = true_monkey
        self.false_monkey: int = false_monkey

    @staticmethod
    def parse_and_create_monkey(monkey_data: List[str]):
        regex = (
            r"Monkey (\d+):\n  Starting items: (.*)\n"
            r"  Operation: new = (\w+) (\W) (\w+)\n"
            r"  Test: divisible by (\d+)\n"
            r"    If true: throw to monkey (\d+)\n"
            r"    If false: throw to monkey (\d+)"
        )
        
        expr = re.search(regex, monkey_data, re.MULTILINE)
        monkey_id: str = expr.group(1)
        items: str = expr.group(2)
        op1: List[str] = expr.group(3)
        op2: List[str] = expr.group(4)
        op3: List[str] = expr.group(5)
        test_divisible: str = expr.group(6)
        true_monkey: str = expr.group(7)
        false_monkey: str = expr.group(8)

        return Monkey(
            id=int(monkey_id),
            items=[int(item) for item in items.split(",")],
            operation=[op1, op2, op3],
            test_divisible=int(test_divisible),
            true_monkey=int(true_monkey),
            false_monkey=int(false_monkey),
        )

    def new_worry_level(self, item: int) -> int:
        operand1 = self.operation[0]  # old
        operator = self.operation[1]  # '+' or '*'
        operand2 = self.operation[2]  # old or a number

        if operand2.isnumeric():
            operand2 = int(operand2)
        else:
            operand2 = item

        if operator == "+":
            return item + operand2
        if operator == "*":
            return item * operand2

    def __str__(self) -> str:
        return f"{self.id = }, {self.items = } {self.operation} {self.test_divisible = } {self.true_monkey = } {self.false_monkey = }"


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read()

    monkeys_raw_data: List[str] = data.split("\n\n")
    monkeys: Dict[int, Monkey] = {}
    monkey_inspection: Dict[int, int] = {}
    for monkey_id, monkey_data in enumerate(monkeys_raw_data):
        monkeys[monkey_id] = Monkey.parse_and_create_monkey(monkey_data)
        monkey_inspection[monkey_id] = 0

    adjustment = 1
    for monkey in monkeys.values():
        adjustment *= monkey.test_divisible

    for game_round in range(1, 10_001):
    # for game_round in range(1, 21):

        for id, monkey in monkeys.items():
            while monkey.items:
                monkey_inspection[id] += 1
                item = monkey.items.pop()
                item = monkey.new_worry_level(item) # // 3
                item = item % adjustment
                reminder = item % monkey.test_divisible
                if reminder == 0:
                    monkeys[monkey.true_monkey].items.append(item)
                else:
                    monkeys[monkey.false_monkey].items.append(item)

        # if game_round % 1000 == 0:
        #     for monkey_id, inspected in monkey_inspection.items():
        #         print(f"Monkey {monkey_id} inspected items {inspected} times")

    print(f"{game_round = }")
    for id, monkey in monkeys.items():
        print(id, monkey.items)
    print("----------------------------")


    sort_inspected = sorted(monkey_inspection.values(), reverse=True)
    print(sort_inspected)

    return sort_inspected[0] * sort_inspected[1]


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 2713310158

    result = solution("./input.txt")
    print(result)
