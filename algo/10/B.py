from typing import Optional, Union, Tuple, List
import sys
from sys import setrecursionlimit
import threading
from io import IOBase, BytesIO
from os import read, write, fstat
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


class Graph:
    """Граф"""
    def __init__(self, number_of_vertices: int) -> None:
        if number_of_vertices <= 0:
            raise ValueError("number of vertices should be greater than 0")
        self.edges = [[] for _ in range(number_of_vertices)]
        self.number_of_vertices = number_of_vertices

    def add_edge(self, a: int, b: int) -> None:
        """Добавление ребра"""
        a -= 1
        b -= 1
        if max(a, b) > self.number_of_vertices:
            raise ValueError("a and b should be less than or equal number of vertices")
        self.edges[a].append(b)

    def __max_depth_helper(self, vertex: int, depth: int = 1, depths: Optional[List] = None) -> int:
        """Поиск максимальной глубины"""
        if depths is None:
            depths = []
        if not self.edges[vertex]:
            depths.append(depth)
        for u in self.edges[vertex]:
            self.__max_depth_helper(u, depth + 1, depths)
        return max(depths)

    def max_depth(self, vertex: int) -> int:
        """Поиск максимальной глубины"""
        return self.__max_depth_helper(vertex)


def main() -> None:
    """Чтение, обработка, вывод"""
    number_of_reposts = int(_input())
    edges = []
    encoded_names = {}
    counter = 0
    for _ in range(number_of_reposts):
        name1, _, name2 = _input().lower().split()
        if name1 not in encoded_names:
            counter += 1
            encoded_names[name1] = counter
        if name2 not in encoded_names:
            counter += 1
            encoded_names[name2] = counter
        edges.append((encoded_names[name2], encoded_names[name1]))
    graph = Graph(counter)
    for edge in edges:
        graph.add_edge(*edge)
    res = graph.max_depth(1)
    stdout.write(f"{res}")


if __name__ == "__main__":
    setrecursionlimit(10 ** 9)
    threading.stack_size(2 ** 26)  # лучше использовать именно эту константу
    thread = threading.Thread(target=main)
    thread.start()
