from sys import stdin, stdout
from typing import List, Tuple


def values_range(arr: List[int]) -> Tuple[int, int]:
    """Крайние значения массива"""
    return min(arr), max(arr)


def cnt_sort(arr: List[int], vals_range: Tuple[int, int]) -> None:
    """Сортировка подсчетом"""
    min_el, max_el = vals_range
    cnt_length = max_el - min_el + 1  # определяем размер массива для подсчета
    cnt = [0] * cnt_length

    for a in arr:
        cnt[a - min_el] += 1  # отображаем [min..max] -> [0..max - min]

    i = 0
    for j in range(cnt_length):  # распаковываем cnt в исходный массив
        while cnt[j] > 0:
            arr[i] = j + min_el  # отображаем обратно [0..max - min] -> [min..max]
            i += 1
            cnt[j] -= 1


if __name__ == '__main__':
    array = [int(a) for a in stdin.readline().split()]
    cnt_sort(array, vals_range=values_range(array))
    stdout.write(' '.join(map(str, array)))
