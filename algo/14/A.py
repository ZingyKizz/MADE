import sys
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


def _input():
    return stdin.readline().rstrip()


def split_input():
    return _input().split()


def fast_print(*args, sep=" ", end="\n"):
    for a in args:
        stdout.write(f"{a}{sep}")
    stdout.write(f"{end}")
#################################################################################


class Solver:
    """Решала"""
    P = 29
    M = 10 ** 13

    def __init__(self, string: str) -> None:
        hashes = [None] * len(string)
        powers = [None] * len(string)
        hashes[0] = ord(string[0])
        powers[0] = 1
        for i in range(1, len(string)):
            hashes[i] = (hashes[i - 1] * self.P + ord(string[i])) % self.M
            powers[i] = (powers[i - 1] * self.P) % self.M
        self.hashes = hashes
        self.powers = powers

    def get_hash(self, left: int, right: int) -> int:
        """Получение хэша по индексам подстроки"""
        if left == 0:
            return self.hashes[right]
        return (self.hashes[right] - self.hashes[left - 1] * self.powers[right - left + 1]) % self.M

    def check_equality(self, a: int, b: int, c: int, d: int) -> None:
        """Проверка на равенство"""
        a -= 1
        b -= 1
        c -= 1
        d -= 1
        fast_print("Yes" if self.get_hash(a, b) == self.get_hash(c, d) else "No")


def main() -> None:
    """Считывание, обработка, вывод"""
    string = _input()
    solver = Solver(string)
    queries_number = int(_input())
    for _ in range(queries_number):
        solver.check_equality(*map(int, split_input()))


if __name__ == "__main__":
    main()
