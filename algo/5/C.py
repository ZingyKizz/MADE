################################################################################
"""Обертка для быстрого ввода/вывода"""
import sys
from io import IOBase, BytesIO
from os import read, write, fstat
from typing import Optional, Union

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
    def __init__(
            self, insert_order: Optional[int] = None, key: Optional[str] = None, value: Optional[str] = None,
            prev_node: Optional["Node"] = None, next_node: Optional["Node"] = None
    ) -> None:
        self.insert_order = insert_order
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

    def add(self, insert_order: int, key: str, value: str) -> Optional[int]:
        """Добавляет значение value"""
        if self.head.key is None:
            self.head = Node(insert_order, key, value)
        elif self.head.key == key:
            self.head.value = value
            return self.head.insert_order
        else:
            cur = self.head
            while cur.next_node is not None:
                cur = cur.next_node
                if cur.key == key:
                    cur.value = value
                    return cur.insert_order
            cur.next_node = Node(insert_order, key, value, cur)
        return None

    def remove(self, key: str) -> Optional[int]:
        """Удаляет связку с ключом key"""
        cur = self.head
        if cur.key == key:
            removed_insert_order = self.head.insert_order
            self.head = self.head.next_node or Node()
            return removed_insert_order
        while cur.next_node is not None:
            cur = cur.next_node
            if cur.key == key:
                removed_insert_order = cur.insert_order
                if cur.next_node is None:
                    cur.prev_node.next_node = None
                else:
                    cur.next_node.prev_node = cur.prev_node
                    cur.prev_node.next_node = cur.next_node
                return removed_insert_order
        return None

    def get(self, key: str, default_value: Optional[str] = None, rtrn_insert_order: bool = False) -> Union[str, int]:
        """Возвращает значение по ключу key"""
        cur = self.head
        while cur.next_node is not None and cur.key != key:
            cur = cur.next_node
        if rtrn_insert_order:
            res = cur.insert_order if cur.key == key else default_value
        else:
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

    def __init__(self, number_of_operations) -> None:
        self.capacity = self.PRIME
        self.container = [LinkedList() for _ in range(self.capacity)]
        self.order_values = [None] * number_of_operations
        self.current_insert_order = 0

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
        overwrited_insert_order = ll.add(self.current_insert_order, key, value)
        if overwrited_insert_order is not None:
            self.order_values[overwrited_insert_order] = value
        else:
            self.order_values[self.current_insert_order] = value
            self.current_insert_order += 1

    def remove(self, key: str) -> None:
        """Удаляет значение value из множества"""
        addr = self._hash(key)
        ll = self.container[addr]
        removed_insert_order = ll.remove(key)
        if removed_insert_order is not None:
            self.order_values[removed_insert_order] = None

    def get(self, key: str, default: Optional[str] = None) -> Union[str, int]:
        """Возвращает значение по ключу key"""
        addr = self._hash(key)
        ll = self.container[addr]
        res = ll.get(key, default)
        return res

    def next(self, key, default: Optional[str] = None) -> Optional[str]:
        """Возвращает значение по первому ключу, вставленному после key"""
        addr = self._hash(key)
        ll = self.container[addr]
        insert_order = ll.get(key, rtrn_insert_order=True)
        if insert_order is not None:
            if not insert_order + 1 >= self.current_insert_order:
                for i in range(insert_order + 1, self.current_insert_order):
                    cur = self.order_values[i]
                    if cur is not None:
                        return cur
        return default

    def prev(self, key, default: Optional[str] = None) -> Optional[str]:
        """Возвращает значение по последнему ключу, вставленному до key"""
        addr = self._hash(key)
        ll = self.container[addr]
        insert_order = ll.get(key, rtrn_insert_order=True)
        if insert_order is not None:
            if insert_order > 0:
                for i in range(insert_order - 1, -1, -1):
                    cur = self.order_values[i]
                    if cur is not None:
                        return cur
        return default


def main() -> None:
    """Считывание, обработка, вывод"""
    NUMBER_OF_OPERATIONS = 10 ** 6

    hash_map = Map(NUMBER_OF_OPERATIONS)
    for operation in stdin:
        oper = operation.strip("\r\n").split()
        action, args = oper[0], oper[1:]
        if action == "put":
            hash_map.add(*args)
        elif action == "delete":
            hash_map.remove(*args)
        elif action == "get":
            res = hash_map.get(*args, "none")
            stdout.write(res + "\n")
        elif action == "prev":
            res = hash_map.prev(*args, "none")
            stdout.write(res + "\n")
        elif action == "next":
            res = hash_map.next(*args, "none")
            stdout.write(res + "\n")


if __name__ == "__main__":
    main()
