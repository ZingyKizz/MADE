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


def split_input():
    return stdin.readline().split()


def _input():
    return stdin.readline()
#################################################################################


class FenwickTree:
    """Дерево Фенвика"""
    @staticmethod
    def _fenwick_and(val: int) -> int:
        """Функция с побитовым 'и' для реализации методов"""
        return val & (val + 1)

    @staticmethod
    def _fenwick_or(val: int) -> int:
        """Функция с побитовым 'или' для реализации методов"""
        return val | (val + 1)

    def __init__(self, array: List[int]) -> None:
        self.array = array[:]
        self.size = len(self.array)
        self.prefix_sum = [None] * self.size
        for i in range(self.size):
            self.prefix_sum[i] = sum(array[j] for j in range(self._fenwick_and(i), i + 1))

    def _sum(self, right: int) -> int:
        """Возвращает сумму на отрезке [0, right]"""
        res = 0
        while right >= 0:
            res += self.prefix_sum[right]
            right = self._fenwick_and(right) - 1
        return res

    def sum(self, left: int, right: int) -> int:
        """Возвращает сумму на отрезке [left, right]"""
        return self._sum(right) - self._sum(left - 1)

    def add(self, idx: int, val: int) -> None:
        """Добавляет к элементу с индексом idx значение val"""
        self.array[idx] += val
        while idx < self.size:
            self.prefix_sum[idx] += val
            idx = self._fenwick_or(idx)

    def __getitem__(self, idx: int) -> int:
        return self.array[idx]

    def __setitem__(self, idx: int, val: int) -> None:
        diff = val - self.array[idx]
        self.add(idx, diff)


def main() -> None:
    """Считывание, обработка, вывод"""
    _ = int(_input())
    array = [int(x) for x in split_input()]
    ft = FenwickTree(array)
    for operation in stdin:
        description, *args = operation.split()
        if description == "sum":
            left, right = map(lambda x: int(x) - 1, args)
            res = ft.sum(left, right)
            stdout.write(f"{res}\n")
        elif description == "set":
            idx_, val = map(int, args)
            idx = idx_ - 1
            ft[idx] = val


if __name__ == "__main__":
    main()
