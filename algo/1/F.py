from sys import stdin, stdout
from functools import lru_cache
from typing import List, Tuple

ROMAN_INT_MAP = {  # Маппинг: римская цифра - int
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50
}


def get_int(roman_digit):
    """Римская цифра -> int"""
    return ROMAN_INT_MAP.get(roman_digit)


def max_roman_digit(string: str) -> Tuple[int, int]:
    """Находим индекс и int-значение наибольшей римской цифры в числе"""
    max_idx = 0
    max_val = string[0]
    if len(string) > 1:
        for i, a in enumerate(string[1:], 1):
            if get_int(a) > get_int(max_val):
                max_idx = i
                max_val = a
    return max_idx, get_int(max_val)


@lru_cache(maxsize=50)
def roman_number_to_int(roman: str) -> int:
    """Переводим число из римских цифр в int"""
    if len(roman) == 0:
        return 0
    max_idx, ans = max_roman_digit(roman)
    left, right = roman[:max_idx], roman[max_idx + 1:]
    ans += roman_number_to_int(right)
    ans -= roman_number_to_int(left)
    return ans


def king_sort(kings: List[str]) -> List[str]:
    """Сортируем королей"""
    sorted_pairs = sorted([king.split() for king in kings], key=lambda x: (x[0], roman_number_to_int(x[1])))
    ans = [f'{pair[0]} {pair[1]}' for pair in sorted_pairs]
    return ans


if __name__ == '__main__':
    n = int(stdin.readline())
    kings_list = [stdin.readline() for _ in range(n)]
    for k in king_sort(kings_list):
        stdout.write(k + '\n')
