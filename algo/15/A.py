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


class Lexer:
    """Лексер"""
    OPERATORS = set("()+-*/")

    def __init__(self, string: str) -> None:
        self.string = string
        self.tokens = self.evaluate()
        self.size = len(self.tokens)
        self.__current_index = 0

    def evaluate(self) -> List[str]:
        """Токенизация"""
        res = []
        buffer = []
        for c in self.string:
            if c in self.OPERATORS:
                if buffer:
                    res.append("".join(buffer))
                    buffer.clear()
                res.append(c)
            elif c == ".":
                res.append("".join(buffer))
                break
            else:
                buffer.append(c)
        return res

    def next_token(self) -> str:
        """Следующий токен"""
        if self.__current_index < self.size:
            res = self.tokens[self.__current_index]
            self.__current_index += 1
            return res

    def print(self) -> None:
        """Вывод"""
        for _ in range(self.size):
            current_token = self.next_token()
            fast_print(current_token)


def main() -> None:
    """Считывание, обработка, вывод"""
    string = _input()
    lexer = Lexer(string)
    lexer.print()


if __name__ == "__main__":
    main()
