from typing import Optional, Union, Tuple, List
import sys
from sys import setrecursionlimit
import threading
from io import IOBase, BytesIO
from os import read, write, fstat
from collections import defaultdict, deque

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
        self.__seen = [False] * number_of_vertices

    def add_edge(self, a: int, b: int, w: int) -> None:
        """Добавление ребра"""
        a -= 1
        b -= 1
        if max(a, b) > self.number_of_vertices:
            raise ValueError("a and b should be less than or equal number of vertices")
        self.edges[a].append((b, w))
        self.edges[b].append((a, w))

    def dijkstra(self, start):
        start -= 1
        distances = [float("inf")] * self.number_of_vertices
        distances[start] = 0
        for i in range(self.number_of_vertices):
            nxt = -1
            for v in range(self.number_of_vertices):
                if (nxt == -1 or distances[v] < distances[nxt]) and not self.__seen[v]:
                    nxt = v
            if distances[nxt] == float("inf"):
                break
            self.__seen[nxt] = True
            for u, weight in self.edges[nxt]:
                distances[u] = min(distances[u], distances[nxt] + weight)
        return distances


def main() -> None:
    """Чтение, обработка, вывод"""
    number_of_vertices, number_of_edges = map(int, split_input())
    graph = Graph(number_of_vertices)
    for _ in range(number_of_edges):
        u, v, w = map(int, split_input())
        graph.add_edge(u, v, w)
    res = graph.dijkstra(1)
    print(*res)


if __name__ == "__main__":
    main()
