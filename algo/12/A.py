import sys
from io import IOBase, BytesIO
from os import read, write, fstat
from typing import Optional
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


def split_input():
    return stdin.readline().split()


def _input():
    return stdin.readline()


def fast_print(*args, sep=" ", end="\n"):
    for a in args:
        stdout.write(f"{a}{sep}")
    stdout.write(f"{end}")
#################################################################################


class DisjointSet:
    """Система непересекающихся множеств"""
    def __init__(self, number_of_elements: int) -> None:
        self.ancestors = [i for i in range(number_of_elements)]
        self.max = [i for i in range(number_of_elements)]
        self.min = [i for i in range(number_of_elements)]
        self.count = [1] * number_of_elements

    def _search(self, x: int, first: bool = True) -> int:
        """Поиск"""
        if first:
            x -= 1
        if self.ancestors[x] == x:
            return x
        first = False
        return self._search(self.ancestors[x], first)

    def join(self, x: int, y: int) -> None:
        """Объединение"""
        x = self._search(x)
        y = self._search(y)
        if x == y:
            return
        if self.count[x] < self.count[y]:
            x, y = y, x
        self.count[x] += self.count[y]
        if self.max[x] < self.max[y]:
            self.max[x] = self.max[y]
        else:
            self.max[y] = self.max[x]
        if self.min[x] > self.min[y]:
            self.min[x] = self.min[y]
        else:
            self.min[y] = self.min[x]
        self.ancestors[y] = x

    def get(self, x: int) -> None:
        """Вывод инфо"""
        x = self._search(x)
        fast_print(self.min[x] + 1, self.max[x] + 1, self.count[x])


def main() -> None:
    """Считывание, обработка, вывод"""
    number_of_elements = int(_input())
    ds = DisjointSet(number_of_elements)
    for operation in stdin:
        action, *args = operation.rstrip("\n").split()
        if action == "union":
            ds.join(*map(int, args))
        elif action == "get":
            ds.get(int(*args))


if __name__ == "__main__":
    main()
