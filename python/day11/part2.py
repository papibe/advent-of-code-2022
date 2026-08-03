import re
from typing import Dict, List, Match, Optional


class Monkey:
    def __init__(
        self,
        monkey_id: int,
        items: List[int],
        operation: List[str],
        test_divisible: int,
        true_monkey: int,
        false_monkey: int,
    ) -> None:
        self.id: int = monkey_id
        self.items: List[int] = items
        self.operation: List[str] = operation
        self.test_divisible: int = test_divisible
        self.true_monkey: int = true_monkey
        self.false_monkey: int = false_monkey

    @staticmethod
    def from_text(monkey_data: str) -> "Monkey":
        regex: str = (
            r"Monkey (\d+):\n  Starting items: (.*)\n"
            r"  Operation: new = (\w+) (\W) (\w+)\n"
            r"  Test: divisible by (\d+)\n"
            r"    If true: throw to monkey (\d+)\n"
            r"    If false: throw to monkey (\d+)"
        )
        matches: Optional[Match[str]] = re.match(regex, monkey_data, re.MULTILINE)
        if matches:
            monkey_id: str = matches.group(1)
            items: str = matches.group(2)
            op1: str = matches.group(3)
            op2: str = matches.group(4)
            op3: str = matches.group(5)
            test_divisible: str = matches.group(6)
            true_monkey: str = matches.group(7)
            false_monkey: str = matches.group(8)

        return Monkey(
            monkey_id=int(monkey_id),
            items=[int(item) for item in items.split(",")],
            operation=[op1, op2, op3],
            test_divisible=int(test_divisible),
            true_monkey=int(true_monkey),
            false_monkey=int(false_monkey),
        )

    def new_worry_level(self, item: int) -> int:
        _, operator, str_operand = self.operation
        operand: int = int(str_operand) if str_operand.isnumeric() else item
        return item + operand if operator == "+" else item * operand


def parse(filename: str) -> List[Monkey]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().split("\n\n")

    monkeys: List[Monkey] = []
    for data_block in data:
        monkeys.append(Monkey.from_text(data_block))

    return monkeys


def solve(monkeys: List[Monkey]) -> int:
    # create game objects
    monkey_inspections: Dict[int, int] = {}
    for monkey in monkeys:
        monkey_inspections[monkey.id] = 0

    # calculate bound for worry level: create LCM for primes
    adjustment: int = 1
    for monkey in monkeys:
        adjustment *= monkey.test_divisible

    # play game
    for _ in range(10_000):
        for monkey in monkeys:
            while monkey.items:
                monkey_inspections[monkey.id] += 1
                original_item: int = monkey.items.pop()
                new_item: int = monkey.new_worry_level(original_item) % adjustment

                if new_item % monkey.test_divisible == 0:
                    monkeys[monkey.true_monkey].items.append(new_item)
                else:
                    monkeys[monkey.false_monkey].items.append(new_item)

    sort_inspected: List[int] = sorted(monkey_inspections.values(), reverse=True)
    return sort_inspected[0] * sort_inspected[1]


def solution(filename: str) -> int:
    monkeys: List[Monkey] = parse(filename)
    return solve(monkeys)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 2713310158
    print(solution("./input.txt"))  # 20683044837
