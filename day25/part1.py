from typing import List

TRANS = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

RETRANS = {
    2: "2",
    1: "1",
    0: "0",
    -1: "-",
    -2: "=",
}


def parse(filename: str) -> List[str]:
    with open(filename, "r") as file:
        data = file.read().splitlines()
    return data


def number_to_snafu2(number: int) -> str:
    snafu: List[int] = [0] * 30
    index: int = 0
    exponent: int = 1
    while number > 0:
        # digit = number // 5
        reminder = number % 5
        print(f"{number = }, {5 ** exponent = }, {reminder = }")
        if reminder > 2:
            print(f"{reminder = }")
            snafu[index + 1] += 1
            print((reminder * (5**exponent)), (5 ** (exponent + 1)))
            reminder = ((reminder * (5**exponent)) - (5 ** (exponent + 1))) // (
                5**exponent
            )
            # reminder -= 5
            print(f"{reminder = }")
        snafu[index] += reminder
        print(snafu)
        index += 1
        exponent += 1
        number //= 5
        print()

    # if snafu[index] != 0:
    #     index += 1

    # print(snafu)
    # while True:
    #     if snafu[-1] != "0":
    #         break
    #     snafu.pop()

    return "".join(reversed([f"{RETRANS[n]}" for n in snafu[: index + 1]]))


def number_to_snafu3(number: int) -> str:
    snafu: List[int] = [0] * 30
    index: int = 0
    exponent: int = 1
    while number > 0:
        # digit = number // 5
        reminder = number % 5
        print(f"{number = }, {5 ** exponent = }, {reminder = }, {snafu[index]}")
        snafu[index] += reminder
        reminder = snafu[index]
        if reminder > 2:
            print(f"{reminder = }")
            snafu[index + 1] += 1
            # number += 5 ** (exponent + 1)
            print((reminder * (5**exponent)), (5 ** (exponent + 1)))
            reminder = ((reminder * (5**exponent)) - (5 ** (exponent + 1))) // (
                5**exponent
            )
            # reminder -= 5
            print(f"{reminder = }")
            snafu[index] = reminder
        print(snafu)
        index += 1
        exponent += 1
        number //= 5
        print()
    
    return "".join(reversed([f"{RETRANS[n]}" for n in snafu[: index + 1]]))
    # return "".join(reversed([f"{RETRANS[n]}" for n in snafu]))


def number_to_snafu(number: int) -> str:
    snafu: List[int] = [0] * 30
    index: int = 0
    exponent: int = 1
    while number > 0:
        reminder = number % 5
        snafu[index] += reminder
        reminder = snafu[index]
        if reminder > 2:
            snafu[index + 1] += 1
            # reminder = (reminder * (5**exponent)) - (5 ** (exponent + 1)) // (
            #     5**exponent
            # )
            reminder -= 5
            snafu[index] = reminder
        index += 1
        exponent += 1
        number //= 5

    while snafu[-1] == 0:
        snafu.pop()

    # return "".join(reversed([f"{RETRANS[n]}" for n in snafu[: index + 1]]))
    return "".join(reversed([f"{RETRANS[n]}" for n in snafu]))


def translate(snafu: str) -> int:

    number: int = 0
    exponent: int = 0

    for index in range(len(snafu) - 1, -1, -1):
        number += TRANS[snafu[index]] * (5**exponent)
        # print(snafu[index], TRANS[snafu[index]] * (5 ** exponent))
        exponent += 1

    return number


def solve(numbers: List[str]) -> str:
    total_sum: int = 0
    for snafu_number in numbers:
        # print(snafu_number, "\t",translate(snafu_number))
        total_sum += translate(snafu_number)
    return number_to_snafu(total_sum)


def solution(filename: str) -> str:
    test_data = [
        [1, "1"],
        [2, "2"],
        [3, "1="],
        [4, "1-"],
        [5, "10"],
        [6, "11"],
        [7, "12"],
        [8, "2="],
        [9, "2-"],
        [10, "20"],
        [15, "1=0"],
        [20, "1-0"],
        [2022, "1=11-2"],
        [12345, "1-0---0"],
        [314159265, "1121-1110-1=0"],
        [4890, "2=-1=0"],
    ]
    # for number, expected_snafu in test_data:
    #     print(f"{number = }\n-----------------------------------------")
    #     snafu = number_to_snafu(number)
    #     print("res", number, expected_snafu, snafu)
    # return 0
    numbers = parse(filename)
    # print("2=-01", translate("2=-01"))
    # return 0
    return solve(numbers)


if __name__ == "__main__":
    print(solution("./example.txt"))
    print(solution("./input.txt"))
