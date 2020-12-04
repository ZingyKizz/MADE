import sys
from io import IOBase, BytesIO
from os import read, write, fstat
from typing import Optional
from functools import total_ordering
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


@total_ordering
class Edge:
    """Ребро"""
    def __init__(self, u: int, v: int, weight: int) -> None:
        self.u = u
        self.v = v
        self.weight = weight

    def __eq__(self, other: "Edge") -> bool:
        return self.weight == other.weight

    def __lt__(self, other: "Edge") -> bool:
        return self.weight < other.weight


class Graph:
    """Граф"""
    def __init__(self, number_of_vertices: int) -> None:
        self.edges = []
        self.ancestors = [i for i in range(number_of_vertices)]
        self.count = [1] * number_of_vertices

    def add_edge(self, u: int, v: int, weight: int) -> None:
        """Добавление ребра"""
        u -= 1
        v -= 1
        edge = Edge(u, v, weight)
        self.edges.append(edge)

    def _search(self, u: int, first: bool = True) -> int:
        """Поиск"""
        if first:
            u -= 1
        if self.ancestors[u] == u:
            return u
        first = False
        return self._search(self.ancestors[u], first)

    def _join(self, u: int, v: int) -> None:
        """Объединение"""
        u = self._search(u)
        v = self._search(v)
        if self.count[u] < self.count[v]:
            u, v = v, u
        self.count[u] += self.count[v]
        self.ancestors[v] = u

    def kruskal(self) -> None:
        """Вывод веса легчайшего остовного дерева"""
        self.edges.sort()
        res = 0
        for edge in self.edges:
            if self._search(edge.u) != self._search(edge.v):
                res += edge.weight
                self._join(edge.u, edge.v)
        fast_print(res)


def main() -> None:
    """Считывание, обработка, вывод"""
    number_of_elements, number_of_edges = map(int, split_input())
    graph = Graph(number_of_elements)
    for i in range(number_of_edges):
        graph.add_edge(*map(int, split_input()))
    graph.kruskal()


if __name__ == "__main__":
    main()
