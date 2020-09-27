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


def check_answer(arr: List[int], rope_len: int, houses_num: int) -> bool:
    """Проверка, что можно нарезать в домики по веревке длины rope_len"""
    for a in arr:
        houses_num -= a // rope_len
        if houses_num <= 0:
            return True
    return False


def ans_bin_search(arr: List[int], houses_num: int, left: int, right: int) -> int:
    """Бинарный поиск по ответу"""
    while not right - left <= 1:
        border = (right + left) // 2
        if check_answer(arr, border, houses_num):
            left = border
        else:
            right = border
    return right - 1


def main() -> None:
    """Считывание, обработка, вывод"""
    n, k = inpt()

    array = []
    for _ in range(n):
        array.append(inpt(False))
    array.sort(reverse=True)

    LFT = 0
    rght = sum(array) // k + 1
    ans = ans_bin_search(array, k, left=LFT, right=rght)
    prnt(ans)


if __name__ == '__main__':
    main()
