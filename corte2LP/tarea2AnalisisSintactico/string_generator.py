import random


def generate_expression(length: int) -> str:
    expr = ""
    for i in range(length):
        expr += str(random.randint(0, 9))
        if i < length - 1:
            expr += random.choice(["+", "*"])
    return expr
