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
        self.size = 1


class CartesianTree:
    """Декартово дерево"""
    def __init__(self) -> None:
        self.root = None

    @staticmethod
    def _get_size(node: Optional["BinaryNode"]) -> int:
        """Размер"""
        if node is None:
            return 0
        return node.size

    @staticmethod
    def _fix_size(node: Optional["BinaryNode"]) -> None:
        """Обновление размера"""
        node.size = CartesianTree._get_size(node.left) + CartesianTree._get_size(node.right) + 1

    @staticmethod
    def _split(node: Optional["BinaryNode"], value: int) -> Tuple[Optional["BinaryNode"], Optional["BinaryNode"]]:
        """Разбиение по значению"""
        if node is None:
            return None, None
        if CartesianTree._get_size(node.left) >= value:
            tree1, node.left = CartesianTree._split(node.left, value)
            CartesianTree._fix_size(node)
            return tree1, node
        node.right, tree2 = CartesianTree._split(node.right, value - CartesianTree._get_size(node.left) - 1)
        CartesianTree._fix_size(node)
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
            CartesianTree._fix_size(tree1)
            return tree1
        tree2.left = CartesianTree._merge(tree1, tree2.left)
        CartesianTree._fix_size(tree2)
        return tree2

    @staticmethod
    def _insert(node: Optional["BinaryNode"], idx: int, value: int) -> "BinaryNode":
        """Вставка значения"""
        tree1, tree2 = CartesianTree._split(node, idx)
        tree = CartesianTree._merge(tree1, BinaryNode(value))
        return CartesianTree._merge(tree, tree2)

    @staticmethod
    def _delete(node: Optional["BinaryNode"], idx: int) -> Optional["BinaryNode"]:
        """Удаление значения"""
        tree1, tree2 = CartesianTree._split(node, idx)
        _, tree22 = CartesianTree._split(tree2, 1)
        return CartesianTree._merge(tree1, tree22)

    @staticmethod
    def _print(node: Optional["BinaryNode"]) -> None:
        """Вывод"""
        if node is None:
            return
        CartesianTree._print(node.left)
        stdout.write(f"{node.value} ")
        CartesianTree._print(node.right)

    def insert(self, idx, value: int) -> None:
        """Вставка значения в дерево"""
        self.root = self._insert(self.root, idx, value)

    def delete(self, idx: int) -> None:
        """Удаление значения из дерева"""
        self.root = self._delete(self.root, idx)

    def build(self, array) -> None:
        """Построение дерева из массива"""
        self.root = None
        for a in array:
            self.root = CartesianTree._merge(self.root, BinaryNode(a))

    def print(self) -> None:
        """Вывод дерева"""
        CartesianTree._print(self.root)

    def print_size(self) -> None:
        """Вывод размера"""
        res = CartesianTree._get_size(self.root)
        stdout.write(f"{res}")


def main() -> None:
    """Чтение, обработка, вывод"""
    ct = CartesianTree()
    array_size, queries_number = map(int, split_input())
    array = map(int, split_input())
    ct.build(array)
    for j in range(queries_number):
        operation, *values_ = split_input()
        values = map(int, values_)
        if operation == "del":
            ct.delete(next(values) - 1)
        elif operation == "add":
            ct.insert(*values)
    ct.print_size()
    stdout.write("\n")
    ct.print()


if __name__ == "__main__":
    main()
