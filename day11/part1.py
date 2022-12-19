import re
import math
from typing import List, Set, Tuple, Dict


class Monkey:
    index = -1

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
        monkey_id: str = re.match("Monkey (\d+):$", monkey_data[0]).group(1)
        str_items = re.match("  Starting items: (.*)$", monkey_data[1]).group(1)
        items = [int(item) for item in str_items.split(",")]
        operation: str = re.match("  Operation: new = (.*)$", monkey_data[2]).group(1)
        test_divisible: str = re.match(
            "  Test: divisible by (\d+)$", monkey_data[3]
        ).group(1)
        true_monkey: str = re.match(
            "    If true: throw to monkey (\d+)$", monkey_data[4]
        ).group(1)
        false_monkey: str = re.match(
            "    If false: throw to monkey (\d+)$", monkey_data[5]
        ).group(1)

        return Monkey(
            id=int(monkey_id),
            items=items,
            operation=operation.split(),
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
    for monkey_id, monkey_data in enumerate(monkeys_raw_data):
        monkeys[monkey_id] = Monkey.parse_and_create_monkey(monkey_data.splitlines())

    for game_round in range(1, 21):
        for monkey in monkeys.values():
            for index, item in enumerate(monkey.items):
                print(monkey.items[index])
                monkey.items[index] = round(monkey.new_worry_level(item) / 3)
                print(monkey.items[index])
                break
            break
        break



    return 0


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)  # it should be 13140

    # result = solution("./input.txt")
    # print(result)
