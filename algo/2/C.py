from sys import stdin, stdout
from itertools import accumulate
from typing import List

ALPH_CNT = 26  # по количеству символов в латинском алфавите


def alph_ord(letter: str) -> int:
    """Маппинг латинских букв в [0, 25]"""
    return ord(letter) - ord('a')


def radix_sort(arr: List[str], k: int) -> List[str]:
    """Цифровая сортировка"""
    for j in range(1, k + 1):
        cnt = [0] * ALPH_CNT
        for a in arr:
            idx = alph_ord(a[-j])
            cnt[idx] += 1

        pos = [0] + [*accumulate(cnt[:-1])]
        arr_ = [None] * len(arr)
        for a in arr:
            idx = alph_ord(a[-j])
            arr_[pos[idx]] = a
            pos[idx] += 1
        arr = arr_

    return arr


if __name__ == '__main__':
    n, _, k_ = map(int, stdin.readline().split())
    array = [stdin.readline().rstrip() for _ in range(n)]
    ans = '\n'.join(radix_sort(array, k_))
    stdout.write(ans)
