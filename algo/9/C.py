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
    def _print(node: Optional["BinaryNode"]) -> None:
        """Вывод"""
        if node is None:
            return
        CartesianTree._print(node.left)
        stdout.write(f"{node.value} ")
        CartesianTree._print(node.right)

    @staticmethod
    def _move_to_start(node: Optional["BinaryNode"], left: int, right: int) -> Optional["BinaryNode"]:
        """Перемещение в начало с индексов left по right"""
        tree1, tree2 = CartesianTree._split(node, right + 1)
        tree11, tree12 = CartesianTree._split(tree1, left)
        tree = CartesianTree._merge(tree12, tree11)
        return CartesianTree._merge(tree, tree2)

    def build(self, array) -> None:
        """Построение дерева из массива"""
        self.root = None
        for a in array:
            self.root = CartesianTree._merge(self.root, BinaryNode(a))

    def move_to_start(self, left: int, right: int) -> None:
        """Перемещение в начало с индексов left по right"""
        self.root = CartesianTree._move_to_start(self.root, left, right)

    def print(self) -> None:
        """Вывод дерева"""
        CartesianTree._print(self.root)


def main() -> None:
    """Чтение, обработка, вывод"""
    ct = CartesianTree()
    array_size, operations_number = map(int, split_input())
    array = list(range(1, array_size + 1))
    ct.build(array)
    for _ in range(operations_number):
        left_, right_ = map(int, split_input())
        ct.move_to_start(left_ - 1, right_ - 1)
    ct.print()


if __name__ == "__main__":
    main()
