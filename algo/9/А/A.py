from typing import Optional, Union, Tuple
import sys
from random import random
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
#################################################################################


class BinaryNode:
    """Бинарный узел"""
    def __init__(self, value: int) -> None:
        self.value = value
        self.key = random() * random()
        self.left = None
        self.right = None


class CartesianTree:
    """Декартово дерево"""
    def __init__(self) -> None:
        self.root = None

    @staticmethod
    def _split(node: Optional["BinaryNode"], value: int) -> Tuple[Optional["BinaryNode"], Optional["BinaryNode"]]:
        """Разбиение по значению"""
        if node is None:
            return None, None
        if node.value > value:
            tree1, node.left = CartesianTree._split(node.left, value)
            return tree1, node
        node.right, tree2 = CartesianTree._split(node.right, value)
        return node, tree2

    @staticmethod
    def _merge(tree1: Optional["BinaryNode"], tree2: Optional["BinaryNode"]) -> "BinaryNode":
        """Слияние"""
        if tree1 is None:
            return tree2
        if tree2 is None:
            return tree1
        if tree1.key > tree2.key:
            tree1.right = CartesianTree._merge(tree1.right, tree2)
            return tree1
        tree2.left = CartesianTree._merge(tree1, tree2.left)
        return tree2

    @staticmethod
    def _insert(node: Optional["BinaryNode"], value: int) -> "BinaryNode":
        """Вставка значения"""
        tree1, tree2 = CartesianTree._split(node, value)
        tree = CartesianTree._merge(tree1, BinaryNode(value))
        return CartesianTree._merge(tree, tree2)

    @staticmethod
    def _delete(node: Optional["BinaryNode"], value: int) -> Optional["BinaryNode"]:
        """Удаление значения"""
        tree1, tree2 = CartesianTree._split(node, value)
        tree11, _ = CartesianTree._split(tree1, value - 1)
        return CartesianTree._merge(tree11, tree2)

    @staticmethod
    def _prev(node: Optional["BinaryNode"], value: int) -> Union[int, str]:
        """Поиск максимального значения, меньше данного"""
        cur = node
        res = "none"
        while cur is not None:
            if cur.value < value:
                res = cur.value
                cur = cur.right
            else:
                cur = cur.left
        return res

    @staticmethod
    def _next(node: Optional["BinaryNode"], value: int) -> Union[int, str]:
        """Поиск минимального значения, больше данного"""
        cur = node
        res = "none"
        while cur is not None:
            if cur.value > value:
                res = cur.value
                cur = cur.left
            else:
                cur = cur.right
        return res

    @staticmethod
    def _exists(node: Optional["BinaryNode"], value: int) -> str:
        """Поиск значения"""
        if node is None:
            return "false"
        elif value < node.value:
            return CartesianTree._exists(node.left, value)
        elif value > node.value:
            return CartesianTree._exists(node.right, value)
        return "true"

    def insert(self, value: int) -> None:
        """Вставка значения в дерево"""
        self.root = self._insert(self.root, value)

    def delete(self, value: int) -> None:
        """Удаление значения из дерева"""
        self.root = self._delete(self.root, value)

    def exists(self, value: int) -> str:
        """Поиск значения по дереву"""
        return self._exists(self.root, value)

    def prev(self, value: int) -> Union[int, str]:
        """Поиск максимального значения, меньше данного"""
        return self._prev(self.root, value)

    def next(self, value: int) -> Union[int, str]:
        """Поиск минимального значения, больше данного"""
        return self._next(self.root, value)


def main() -> None:
    """Чтение, обработка, вывод"""
    ct = CartesianTree()
    for operation in stdin:
        act, val_ = operation.split()
        val = int(val_)
        if act == "insert":
            ct.insert(val)
        elif act == "delete":
            ct.delete(val)
        elif act == "exists":
            res = ct.exists(val)
            stdout.write(f"{res}\n")
        elif act == "prev":
            res = ct.prev(val)
            stdout.write(f"{res}\n")
        elif act == "next":
            res = ct.next(val)
            stdout.write(f"{res}\n")


if __name__ == "__main__":
    main()
