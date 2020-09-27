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


def lower_bound(arr: List[int], val: int) -> int:
    """Левое вхождение val"""
    left = -1
    right = arr.__len__()

    while not right - left <= 1:
        border = (left + right) // 2
        if val <= arr[border]:
            right = border
        else:
            left = border

    return right


def upper_bound(arr: List[int], val: int) -> int:
    """Правое вхождение val"""
    return lower_bound(arr, val + 1)


def count_within(arr: List[int], lower: int, upper: int) -> int:
    """Подсчет количества значений в массиве от lower до upper"""
    return upper_bound(arr, upper) - lower_bound(arr, lower)


def main() -> None:
    """Считывание, обработка, вывод"""
    _ = inpt()
    array = inpt()
    k = inpt(False)
    array.sort()
    for _ in range(k):
        l, r = inpt()
        ans = count_within(array, l, r)
        prnt(ans)


if __name__ == '__main__':
    main()
