import sys
from io import IOBase, BytesIO
from os import read, write, fstat
from typing import List, Optional
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


def find_logs(array_size: int) -> List[Optional[int]]:
    """i-ый элемент означает такое максимальное p, что 2**p <= i"""
    logs = [None] * (array_size + 1)
    logs[1] = 0
    for i in range(2, array_size + 1):
        logs[i] = logs[i // 2] + 1
    return logs


def build_sparse_table(array_size: int, array: List[int], logs) -> List[List[Optional[int]]]:
    """Построение разреженной таблицы"""
    height = logs[array_size] + 1
    sparse_table = [[None] * array_size for _ in range(height)]
    sparse_table[0][:] = array[:]
    for i in range(1, height):
        cur_power = 1 << i
        for j in range(array_size - cur_power + 1):
            sparse_table[i][j] = min(sparse_table[i - 1][j], sparse_table[i - 1][j + cur_power // 2])
    return sparse_table


def find_min(sparse_table: List[List[Optional[int]]], logs: List[int], left: int, right: int) -> int:
    """Поиск минимума на отрезке"""
    p_max = logs[right - left + 1]
    power = 1 << p_max
    min_ = min(sparse_table[p_max][left], sparse_table[p_max][right - power + 1])
    return min_


def main() -> None:
    """Считывание, обработка и вывод"""
    CONST_1 = 23
    CONST_2 = 21563
    CONST_3 = 16714589
    CONST_4 = 17
    CONST_5 = 751
    CONST_6 = 2
    CONST_7 = 13
    CONST_8 = 593
    CONST_9 = 5

    array_size, queries_count, last_element = map(int, split_input())
    array = [None] * array_size
    array[0] = last_element
    for i in range(1, array_size):
        array[i] = (CONST_1 * array[i - 1] + CONST_2) % CONST_3
    logs = find_logs(array_size)
    sparse_table = build_sparse_table(array_size, array, logs)

    left, right = map(int, split_input())
    for i in range(1, queries_count + 1):
        left_ = left - 1
        right_ = right - 1
        if left_ > right_:
            left_, right_ = right_, left_
        cur_min = find_min(sparse_table, logs, left_, right_)
        if i == queries_count:
            res = f"{left} {right} {cur_min}"
            stdout.write(res)
            break
        left = (CONST_4 * left + CONST_5 + cur_min + CONST_6 * i) % array_size + 1
        right = (CONST_7 * right + CONST_8 + cur_min + CONST_9 * i) % array_size + 1


if __name__ == "__main__":
    main()
