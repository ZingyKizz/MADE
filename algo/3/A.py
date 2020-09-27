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


def left_is_closer(arr: List[int], lft: int, rgt: int, val: int) -> bool:
    """Проверка, что значение в левом индексе ближе к val, чем значение в правом индексе"""
    return abs(val - arr[lft]) <= abs(val - arr[rgt])


def search_closest(arr: List[int], val: int) -> int:
    """Приближенный бинарный поиск val на массиве"""
    left = 0
    right = arr.__len__() - 1

    while not right - left <= 1:
        border = (left + right) // 2
        if val <= arr[border]:
            right = border
        else:
            left = border

    return arr[left] if left_is_closer(arr, left, right, val) else arr[right]


def main() -> None:
    """Считывание, обработка, вывод"""
    _ = inpt()
    array, queries = inpt(), inpt()
    for q in queries:
        ans = search_closest(array, q)
        prnt(ans)


if __name__ == '__main__':
    main()
