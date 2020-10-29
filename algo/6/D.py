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
################################################################################


def levenshtein(string1: str, string2: str) -> int:
    """Возвращает расстояние Левенштейна между двумя строками"""
    size1, size2 = len(string1) + 1, len(string2) + 1
    dynamic = [[0] * size2 for _ in range(size1)]

    for i in range(size1):
        dynamic[i][0] = i
    for j in range(size2):
        dynamic[0][j] = j
    for i in range(1, size1):
        for j in range(1, size2):
            penalty = 0 if string1[i - 1] == string2[j - 1] else 1
            dynamic[i][j] = min(dynamic[i - 1][j] + 1, dynamic[i][j - 1] + 1, dynamic[i - 1][j - 1] + penalty)

    distance = dynamic[size1 - 1][size2 - 1]

    return distance


def main() -> None:
    """Считывание, обработка, вывод"""
    string1, string2 = _input().rstrip("\n\r"), _input().rstrip("\n\r")
    ans = levenshtein(string1, string2)
    stdout.write(str(ans))


if __name__ == "__main__":
    main()

