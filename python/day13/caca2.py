from ast import literal_eval


def parse(filename):
    with open(filename, "r") as file:
        data = file.read()  # <--- no splitlines()

    output = []
    for block in data.split("\n\n"):
        output.append([literal_eval(l) for l in block.splitlines()])

    return output


mydata = parse("./input")
