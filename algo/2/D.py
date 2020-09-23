from sys import stdin, stdout
from typing import List

ALPH_CNT = 26  # по количеству символов в латинском алфавите


def alph_ord(letter: str) -> int:
    """Маппинг латинских букв в [0, 25]"""
    return ord(letter) - ord('a')


def is_greater(arr1: List[int], arr2: List[int]) -> bool:
    """Проверка, что элементы первого массива попарно больше или равны элементам второго"""
    assert len(arr1) == len(arr2)
    for a, b in zip(arr1, arr2):
        if a < b:
            return False
    return True


def afterparty(string: str, cards: str) -> int:
    """Считаем подстроки, которые можно составить из карточек"""
    crd_cnt = [0] * ALPH_CNT
    for c in cards:
        crd_cnt[alph_ord(c)] += 1

    ans = left = right = 0
    moved_right = True
    tmp_count = [0] * ALPH_CNT
    while right < len(string):
        if moved_right:
            rgt = string[right]
            tmp_count[alph_ord(rgt)] += 1
        if not is_greater(crd_cnt, tmp_count):
            lft = string[left]
            tmp_count[alph_ord(lft)] -= 1
            left += 1
            moved_right = False
            continue
        ans += right - left + 1
        right += 1
        moved_right = True

    return ans


if __name__ == '__main__':
    _ = stdin.readline()
    string_ = stdin.readline().rstrip()
    cards_ = stdin.readline().rstrip()
    ans_ = afterparty(string_, cards_)
    stdout.write(str(ans_))
