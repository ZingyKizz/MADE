from sys import stdin, stdout
from typing import List


def merge_two_sorted(left: List[int], right: List[int]) -> List[int]:
    """Слияние двух отсортированных массивов в один"""
    arr = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            arr.append(left[i])
            i += 1
        else:
            arr.append(right[j])
            j += 1
    if i < len(left):
        arr.extend(left[i:])
    else:
        arr.extend(right[j:])
    return arr


def merge_sort(arr: List[int]) -> List[int]:
    """Сортировка слиянием"""
    arr_length = len(arr)
    if arr_length > 2:
        border = (arr_length + 1) // 2
        left, right = merge_sort(arr[:border]), merge_sort(arr[border:])
        arr = merge_two_sorted(left, right)
    elif arr_length == 2:
        if arr[0] > arr[1]:
            arr[0], arr[1] = arr[1], arr[0]
    return arr


if __name__ == '__main__':
    _ = stdin.readline()
    array = [int(x) for x in stdin.readline().split()]
    for a in merge_sort(array):
        stdout.write(str(a) + ' ')
