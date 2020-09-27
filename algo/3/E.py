from sys import stdin, stdout
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


def check_answer(copies_number: int, first: int, second: int, time: int) -> bool:
    """Проверка, что можно сделать n копий за время time"""
    time -= min(first, second)
    copies_number -= 1
    return time // first + time // second >= copies_number


def ans_bin_search(copies_number: int, first: int, second: int, left: int, right: int) -> int:
    """Бинарный поиск по ответу"""
    while not right - left <= 1:
        border = (right + left) // 2
        if check_answer(copies_number, first, second, border):
            right = border
        else:
            left = border
    return right


def main() -> None:
    """Считывание, обработка, вывод"""
    n, x, y = inpt()
    LFT = 0
    rght = n * max(x, y)
    ans = ans_bin_search(n, x, y, left=LFT, right=rght)
    prnt(ans)


if __name__ == '__main__':
    main()
