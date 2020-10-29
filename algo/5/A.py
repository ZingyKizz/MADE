import sys
from io import IOBase, BytesIO
from os import read, write, fstat
from typing import Generator, Tuple
################################################################################
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
################################################################################


class Set:
    """Множество на основе хеш-таблицы с использованием открытой адресации"""
    PRIME = 115249

    def __init__(self, number_of_elements: int) -> None:
        self.capacity = 2 * number_of_elements
        self.container = [(None, 0)] * self.capacity

    def _hash(self, value: int) -> int:
        """Хэширует значение"""
        return self.PRIME * value % self.capacity

    def _hashwalk(self, value: int) -> Generator[Tuple[int, int, int], None, None]:
        """Бежит по элементам, начиная с индекса, полученного по хэшу"""
        addr = self._hash(value)
        for i in range(self.capacity):
            idx = (addr + i) % self.capacity
            val, rip = self.container[idx]
            yield idx, val, rip

    def add(self, value: int) -> None:
        """Добавляет элемент value в множество"""
        for cur in self._hashwalk(value):
            idx, val, _ = cur
            if val is None:
                self.container[idx] = value, 0
                return
            elif val == value:
                return

    def exists(self, value: int) -> bool:
        """Проверяет наличие элемента в множестве"""
        for cur in self._hashwalk(value):
            _, val, rip = cur
            if val is None and not rip:
                break
            elif val == value:
                return True
        return False

    def remove(self, value: int) -> None:
        """Удаляет значение value из множества"""
        for cur in self._hashwalk(value):
            idx, val, rip = cur
            if val is None and not rip:
                return
            if val == value:
                self.container[idx] = None, 1

    def __repr__(self) -> str:
        vals = ", ".join(str(i) for i, _ in self.container if i is not None)
        return f"{self.__class__.__name__}({vals})"


def main() -> None:
    """Считывание, обработка, вывод"""
    OPERATIONS = 10 ** 6

    seen = Set(OPERATIONS)

    for operation in stdin:
        act, val_str = operation.rstrip("\n\r").split()
        val = int(val_str)
        if act == "insert":
            seen.add(val)
        elif act == "delete":
            seen.remove(val)
        elif act == "exists":
            res = "true" if seen.exists(val) else "false"
            stdout.write(res + "\n")


if __name__ == "__main__":
    main()
