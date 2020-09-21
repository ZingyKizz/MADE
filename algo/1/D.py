from sys import stdin, stdout
from typing import List, Tuple


def merge_two_sorted_inv(left: List[int], right: List[int]) -> Tuple[List[int], int]:
    """Слияние двух отсортированных массивов в один и подсчет кол-ва инверсий"""
    arr = []
    i = 0
    j = 0
    inv = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            arr.append(left[i])
            i += 1
        else:
            arr.append(right[j])
            j += 1
            inv += len(left) - i
    if i < len(left):
        arr.extend(left[i:])
    else:
        arr.extend(right[j:])
    return arr, inv


def merge_sort_inv(arr: List[int]) -> Tuple[List[int], int]:
    """Сортировка слиянием и подсчет кол-ва инверсий"""
    inv = 0
    arr_length = len(arr)
    if arr_length > 2:
        border = (arr_length + 1) // 2
        left, left_inv = merge_sort_inv(arr[:border])
        right, right_inv = merge_sort_inv(arr[border:])
        arr, inv = merge_two_sorted_inv(left, right)
        inv += (left_inv + right_inv)
    elif arr_length == 2:
        if arr[0] > arr[1]:
            arr[0], arr[1] = arr[1], arr[0]
            inv += 1
    return arr, inv


if __name__ == '__main__':
    _ = stdin.readline()
    array = [int(x) for x in stdin.readline().split()]
    inversions_count = merge_sort_inv(array)[1]
    stdout.write(str(inversions_count))
