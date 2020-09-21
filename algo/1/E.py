from sys import stdin, stdout
import random
from typing import List
 
 
def quick_sort(arr: List[int]) -> List[int]:
    """Быстрая сортировка"""
    if len(arr) < 2:
        return arr
    base = random.choice(arr)
    lower, equal, upper = [], [], []
    for a in arr:
        if a < base:
            lower.append(a)
        elif a == base:
            equal.append(a)
        else:
            upper.append(a)
    return quick_sort(lower) + equal + quick_sort(upper)
 
 
if __name__ == '__main__':
    _ = int(stdin.readline())
    array = [int(x) for x in stdin.readline().split()]
    for el in quick_sort(array):
        stdout.write(str(el) + ' ')
