import sys
from io import IOBase, BytesIO
from os import read, write, fstat
from typing import List
#################################################################################
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
    return stdin.readline().rstrip()


def split_input():
    return _input().split()


def fast_print(*args, sep=" ", end="\n"):
    for a in args:
        stdout.write(f"{a}{sep}")
    stdout.write(f"{end}")
#################################################################################


def prefix_function(string: str) -> List[int]:
    """Префикс-функция"""
    res = [None] * len(string)
    res[0] = 0
    for i in range(1, len(string)):
        k = res[i - 1]
        while k > 0 and string[i] != string[k]:
            k = res[k - 1]
        if string[i] == string[k]:
            k += 1
        res[i] = k
    return res


def search(string: str, pattern: str) -> None:
    """Поиск паттерна в строке"""
    tmp_string = pattern + '#' + string
    prefix = prefix_function(tmp_string)
    res = [i - 2 * len(pattern) for i, p in enumerate(prefix, 1) if p == len(pattern)]
    fast_print(len(res))
    fast_print(*res)


def main() -> None:
    """Считывание, обработка, вывод"""
    pattern, string = _input(), _input()
    search(string, pattern)


if __name__ == "__main__":
    main()
