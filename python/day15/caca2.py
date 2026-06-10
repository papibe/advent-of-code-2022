import re


def parse(filename):
    with open(filename, "r") as file:
        data = file.read().splitlines()

    return [re.findall("-*\d+", line) for line in data]


print(parse("./example.txt"))
