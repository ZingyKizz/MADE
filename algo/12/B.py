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
    """Система непересекающихся множества"""
    def __init__(self, number_of_elements) -> None:
        self.ancestors = [i for i in range(number_of_elements)]
        self.children = [[i] for i in range(number_of_elements)]
        self.count = [1] * number_of_elements
        self.experience = [0] * number_of_elements

    def _search(self, x: int, first: bool = True) -> int:
        """Поиск"""
        if first:
            x -= 1
        if self.ancestors[x] == x:
            return x
        first = False
        return self._search(self.ancestors[x], first)

    def join(self, x: int, y: int) -> Optional[int]:
        """Объединение"""
        x = self._search(x)
        y = self._search(y)
        if x == y:
            return
        if self.count[x] < self.count[y]:
            x, y = y, x
        self.count[x] += self.count[y]
        self.ancestors[y] = x
        for i in self.children[y]:
            self.children[x].append(i)

    def add(self, x: int, exp: int) -> None:
        """Прибавка опыта"""
        x = self._search(x)
        for i in self.children[x]:
            self.experience[i] += exp

    def get(self, x: int) -> None:
        """Вывод инфо"""
        x -= 1
        fast_print(self.experience[x])


def main() -> None:
    """Считывание, обработка, вывод"""
    number_of_elements, number_of_queries = map(int, split_input())
    ds = DisjointSet(number_of_elements)
    for _ in range(number_of_queries):
        action, *args = split_input()
        if action == "join":
            ds.join(*map(int, args))
        elif action == "add":
            ds.add(*map(int, args))
        elif action == "get":
            ds.get(int(*args))


if __name__ == "__main__":
    main()
