from sys import stdin, stdout
from typing import List


def bubble_sort(arr_length, arr: List[int]) -> List[int]:
    """Пузырьковая сортировка"""
    is_sorted = False
    n = 1
    while not is_sorted:
        is_sorted = True
        for i in range(arr_length - n):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False
        n += 1

    return arr


if __name__ == '__main__':
    array_length = int(stdin.readline())
    array = [int(x) for x in stdin.readline().split()]
    for a in bubble_sort(array_length, array):
        stdout.write(str(a) + ' ')
