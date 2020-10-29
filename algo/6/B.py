import sys
from io import IOBase, BytesIO
from os import read, write, fstat
from typing import List, Tuple
from copy import deepcopy
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


def _input():
    return stdin.readline()


def split_input():
    return stdin.readline().split()
################################################################################


def make_directions(path):
    """Возвращает направления R&D из пройденного пути"""
    directions_lst = []
    prev = path[0]
    for p in path[1:]:
        if p > prev:
            directions_lst.append('R')
        else:
            directions_lst.append('D')
        prev = p
    directions = "".join(directions_lst)
    return directions


def maximize_coins(n_rows: int, n_cols: int, coins: List[List[int]]) -> Tuple[int, str]:
    """Возвращает максимальное кол-во монет и направления"""
    dynamic = [[None] * n_cols for _ in range(n_rows)]
    ancestors = deepcopy(dynamic)
    ancestors[n_rows - 1][0] = (n_rows, -1)
    dynamic[n_rows - 1][0] = coins[n_rows - 1][0]

    for i in range(n_rows - 1, -1, -1):
        for j in range(n_cols):
            cur_coins = coins[i][j]
            if i == n_rows - 1 and j > 0:
                dynamic[i][j] = dynamic[i][j - 1] + cur_coins
                ancestors[i][j] = (i, j - 1)
            elif i < n_rows - 1 and j == 0:
                dynamic[i][j] = dynamic[i + 1][j] + cur_coins
                ancestors[i][j] = (i + 1, j)
            elif i < n_rows - 1 and j > 0:
                if dynamic[i + 1][j] > dynamic[i][j - 1]:
                    dynamic[i][j] = dynamic[i + 1][j] + cur_coins
                    ancestors[i][j] = (i + 1, j)
                else:
                    dynamic[i][j] = dynamic[i][j - 1] + cur_coins
                    ancestors[i][j] = (i, j - 1)

    i = 0
    j = n_cols - 1
    path = []
    while i < n_rows and j >= 0:
        path.append((i, j))
        i, j = ancestors[i][j]
    path.reverse()

    directions = make_directions(path)
    max_coins = dynamic[0][n_cols - 1]

    return max_coins, directions


def main() -> None:
    """Считывание, обработка, вывод"""
    n_rows, n_cols = map(int, stdin.readline().split())
    coins = []
    for _ in range(n_rows):
        row = [int(x) for x in split_input()]
        coins.append(row)
    coins.reverse()
    max_coins, directions = maximize_coins(n_rows, n_cols, coins)
    ans = str(max_coins) + "\n" + directions
    stdout.write(ans)


if __name__ == "__main__":
    main()
