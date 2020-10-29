import sys
from io import IOBase, BytesIO
from os import read, write, fstat
from typing import List, Tuple
################################################################################
"""Обертка для быстрого ввода/вывода"""

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = read(self._fd, max(fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self, size: int = ...):
        while self.newlines == 0:
            b = read(self._fd, max(fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


stdin, stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)


def split_input():
    return stdin.readline().split()


def _input():
    return stdin.readline()
################################################################################


def maximize_coins(number_of_pillars: int, max_jump: int, coins: List[int]) -> Tuple[int, int, List[int]]:
    """Возвращает максимальное кол-во монет, количество прыжков и путь"""
    dynamic = [None] * number_of_pillars
    dynamic[0] = 0
    ancestors = dynamic[:]
    coins = [0] + coins + [0]

    for i in range(1, number_of_pillars):
        idx_max = i - 1
        for j in range(max(0, i - max_jump), i - 1):
            if dynamic[j] > dynamic[idx_max]:
                idx_max = j
        dynamic[i] = dynamic[idx_max] + coins[i]
        ancestors[i] = idx_max + 1

    i = number_of_pillars
    path = [i]
    while i > 0:
        i = ancestors[i - 1]
        path.append(i)
    path.pop()
    path.reverse()

    max_coins = dynamic.pop()
    jump_count = len(path) - 1

    return max_coins, jump_count, path


def main() -> None:
    """Считывание, обработка, вывод"""
    number_of_pillars, max_jump = map(int, split_input())
    coins = [int(c) for c in split_input()]
    max_coins, jump_count, path = maximize_coins(number_of_pillars, max_jump, coins)
    ans = str(max_coins) + "\n" + str(jump_count) + "\n" + " ".join(map(str, path))
    stdout.write(ans)


if __name__ == "__main__":
    main()
