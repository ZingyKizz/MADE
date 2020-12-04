import sys
from io import IOBase, BytesIO
from os import read, write, fstat
import itertools
from collections import deque, defaultdict
from typing import Generator
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


class Square:
    """Шахматная клетка"""
    SQUARE_DELTA = [-2, -1, 1, 2]

    def __init__(self, x: int, y: int, n: int) -> None:
        self.x = x
        self.y = y
        self.n = n

    def __check_borders(self, x: int, y: int) -> bool:
        """Проверка на соответствие границам"""
        return (
            1 <= x <= self.n
            and 1 <= y <= self.n
        )

    @property
    def possible_plays(self) -> Generator["Square", None, None]:
        """Генератор следующего хода конем"""
        for x_, y_ in itertools.permutations(self.SQUARE_DELTA, 2):
            if abs(x_) != abs(y_):
                x_new = self.x + x_
                y_new = self.y + y_
                if self.__check_borders(x_new, y_new):
                    new_square = Square(x_new, y_new, self.n)
                    yield new_square

    def __eq__(self, other: "Square") -> bool:
        return (
            self.x == other.x
            and self.y == other.y
            and self.n == other.n
        )

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.n))

    def __repr__(self) -> str:
        return f"{self.x} {self.y}"


class Board:
    """Доска"""
    def __init__(self) -> None:
        self.__seen = set()
        self.__queue = deque()
        self.shortest_distance = defaultdict(lambda: 1)
        self.ancestors = {}

    def bfs(self, square: "Square") -> None:
        """Обход в ширину"""
        self.__seen.add(square)
        self.__queue.append(square)

        while self.__queue:
            current_square = self.__queue.popleft()
            for s in current_square.possible_plays:
                if s not in self.__seen:
                    self.__seen.add(s)
                    self.__queue.append(s)
                    self.shortest_distance[s] = self.shortest_distance[current_square] + 1
                    self.ancestors[s] = current_square

    def print_shortest_route(self, start_square: "Square", end_square: "Square") -> None:
        """Печать посещенных клеток кратчайшего пути"""
        self.bfs(start_square)
        fast_print(self.shortest_distance[end_square])

        route = []
        current_square = end_square
        while True:
            route.append(current_square)
            if current_square == start_square:
                break
            current_square = self.ancestors[current_square]
        fast_print(*reversed(route), sep="\n")


def main() -> None:
    """Чтение, обработка, вывод"""
    n = int(_input())
    start_point = Square(*map(int, split_input()), n)
    end_point = Square(*map(int, split_input()), n)
    board = Board()
    board.print_shortest_route(start_point, end_point)


if __name__ == "__main__":
    main()
