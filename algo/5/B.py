################################################################################
"""Обертка для быстрого ввода/вывода"""
import sys
from io import IOBase, BytesIO
from os import read, write, fstat
from typing import Optional

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


class Node:
    """Узел"""
    def __init__(self, key: Optional[str] = None, value: Optional[str] = None, prev_node: Optional["Node"] = None,
                 next_node: Optional["Node"] = None) -> None:
        self.key = key
        self.value = value
        self.prev_node = prev_node
        self.next_node = next_node

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(key={self.key}, value={self.value})"


class LinkedList:
    """Cвязный список"""
    def __init__(self) -> None:
        self.head = Node()

    def add(self, key: str, value: str) -> None:
        """Добавляет значение value"""
        if self.head.key is None:
            self.head = Node(key, value)
        elif self.head.key == key:
            self.head.value = value
        else:
            cur = self.head
            while cur.next_node is not None:
                cur = cur.next_node
                if cur.key == key:
                    cur.value = value
                    return
            cur.next_node = Node(key, value, cur)

    def remove(self, key: str) -> None:
        """Удаляет связку с ключом key"""
        cur = self.head
        if cur.key == key:
            self.head = self.head.next_node or Node()
            return
        while cur.next_node is not None:
            cur = cur.next_node
            if cur.key == key:
                if cur.next_node is None:
                    cur.prev_node.next_node = None
                else:
                    cur.next_node.prev_node = cur.prev_node
                    cur.prev_node.next_node = cur.next_node
                return

    def get(self, key: str, default_value: Optional[str] = None) -> str:
        """Возвращает значение по ключу key"""
        cur = self.head
        while cur.next_node is not None and cur.key != key:
            cur = cur.next_node
        res = cur.value if cur.key == key else default_value
        return res

    def __repr__(self) -> str:
        vals = ""
        cur = self.head
        if cur.key is not None:
            while cur is not None:
                end = "" if cur.next_node is None else " -> "
                vals += str(cur) + end
                cur = cur.next_node
        return f"{self.__class__.__name__}({vals})"


class Map:
    """Map методом цепочек"""
    ALPHA = 2
    PRIME = 12289

    def __init__(self) -> None:
        self.capacity = self.PRIME
        self.container = [LinkedList() for _ in range(self.capacity)]

    def _hash(self, key: str) -> int:
        """Хэширует значение"""
        res = 0
        for i, s in enumerate(key):
            res += self.ALPHA ** i * ord(s)
        return res % self.capacity

    def add(self, key: str, value: str) -> None:
        """Добавляет элемент value в множество"""
        addr = self._hash(key)
        ll = self.container[addr]
        ll.add(key, value)

    def remove(self, key: str) -> None:
        """Удаляет значение value из множества"""
        addr = self._hash(key)
        ll = self.container[addr]
        ll.remove(key)

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Возвращает значение по ключу key"""
        addr = self._hash(key)
        ll = self.container[addr]
        res = ll.get(key, default)
        return res


def main() -> None:
    """Считывание, обработка, вывод"""
    hash_map = Map()
    for operation in stdin:
        oper = operation.rstrip("\r\n").split()
        action, args = oper[0], oper[1:]
        if action == "put":
            hash_map.add(*args)
        elif action == "delete":
            hash_map.remove(*args)
        elif action == "get":
            res = hash_map.get(*args, "none")
            stdout.write(res + "\n")


if __name__ == "__main__":
    main()
