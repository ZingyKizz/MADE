from sys import stdin, stdout
from typing import Any
from math import log2, ceil
import itertools


def prnt(*args: Any, sep: str = ' ', end: str = '\n') -> None:
    """Быстрый вывод"""
    stdout.write(sep.join(a.__str__() for a in args) + end)


def find_root(precision: float, func: Any, *func_args, left: float = None, right: float = None) -> float:
    """Вещественный двоичный поиск корня непрерывной монотонной неубывающей функции"""
    if left is None:
        left = -1
        while func(left, *func_args) > 0:
            left *= 2
    if right is None:
        right = 1
        while func(right, *func_args) < 0:
            right *= 2

    max_iterations = ceil(log2(abs(left - right) / precision))
    for i in itertools.count():
        border = (left + right) / 2
        if func(border, *func_args) >= 0:
            right = border
        else:
            left = border
        if abs(left - right) < precision or i == max_iterations:
            return left


def main() -> None:
    """Считывание, обработка, вывод"""
    def f(x: float, cnst: float) -> float:
        return x ** 2 + x ** 0.5 - cnst

    PRCSN = 10 ** (-6)
    LFT = 0

    c = float(stdin.readline())
    ans = find_root(PRCSN, f, c, left=LFT)
    prnt(ans)


if __name__ == '__main__':
    main()

