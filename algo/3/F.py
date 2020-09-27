from sys import stdin, stdout
from math import log, ceil
import itertools
from typing import Union, Any, List


def inpt(as_array: bool = True, to_int: bool = True) -> Union[List, Any]:
    """Быстрый ввод"""
    inputline = stdin.readline().rstrip()
    if as_array:
        splitted = inputline.split()
        return [int(x) for x in splitted] if to_int else splitted
    else:
        return int(inputline) if to_int else inputline


def prnt(*args: Any, sep: str = ' ', end: str = '\n') -> None:
    """Быстрый вывод"""
    stdout.write(sep.join(a.__str__() for a in args) + end)


def calc_time(vel_p: int, vel_f: int, forest_start: float, val: float) -> float:
    """Затраченное время при входе в лес в точке val"""
    return ((1 - forest_start) ** 2 + val ** 2) ** 0.5 / vel_p + \
           ((1 - val) ** 2 + forest_start ** 2) ** 0.5 / vel_f


def ternary_search(precision: float, vel_p: int, vel_f: int, forest_start: float, left: float, right: float) -> float:
    """Троичный поиск минимума унимодальной функции"""
    max_iterations = ceil(log(abs(left - right) / precision, 1.5))
    for i in itertools.count():
        border1 = left + (right - left) / 3
        border2 = left + 2 * (right - left) / 3
        if calc_time(vel_p, vel_f, forest_start, border1) < calc_time(vel_p, vel_f, forest_start, border2):
            right = border2
        else:
            left = border1
        if abs(left - right) < precision or i == max_iterations:
            return left


def main() -> None:
    """Считывание, обработка, вывод"""
    vp, vf = inpt()
    a = float(stdin.readline())

    PRCSN = 10 ** (-4)
    LFT = 0
    RGHT = 1
    ans = ternary_search(PRCSN, vp, vf, a, LFT, RGHT)
    prnt(ans)


if __name__ == '__main__':
    main()
