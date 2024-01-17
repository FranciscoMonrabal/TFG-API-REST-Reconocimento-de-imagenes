import math
from sympy.core.sympify import sympify
from sympy import Eq, solve
from sympy.abc import x as X


def replace_posible_equals(equation_string):

    ret = equation_string.replace("--", "=")
    ret = ret.replace("-=", "=")
    ret = ret.replace("==", "=")
    if len(ret.split("=")) > 2:
        raise TypeError("Multiple equal signs, or -- detected")

    return ret


def add_products(equation_string):

    ret = ""
    prev_char = ""

    for char in equation_string:
        if char == "(":
            if prev_char.isnumeric() or prev_char == "x" or prev_char == "(":
                ret += r"*"

        if char == "x":
            if prev_char.isnumeric():
                ret += r"*"

        if prev_char == "x":
            if char.isnumeric():
                ret += r"*"

        if prev_char == ")":
            if char.isnumeric() or char == "x":
                ret += r"*"

        ret += char
        prev_char = char

    return ret


def transform_result_list_into_string(results):

    ret = ""

    for result in results:
        ret += f"x = {result}"

    return ret


def interpret_equation_string(equation_string):

    equation_string = replace_posible_equals(equation_string)
    equation_string = add_products(equation_string)
    print(f"Final equation: {equation_string}")

    equation_splited = equation_string.split("=")
    left_eq = sympify(equation_splited[0])
    right_eq = sympify(equation_splited[1])
    eqn = Eq(left_eq, right_eq)

    return solve(eqn, X)

