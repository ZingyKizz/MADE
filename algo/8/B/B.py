from typing import Optional, Union
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


def split_input():
    return stdin.readline().split()


def _input():
    return stdin.readline()
#################################################################################


class BinaryNode:
    """Бинарный узел"""
    def __init__(self, value: Optional[int] = None) -> None:
        self.value = value
        self.left = None
        self.right = None
        self.height = 0


class AVLTree:
    """Бинарное дерево поиска"""
    def __init__(self) -> None:
        self.root = None

    @staticmethod
    def _height(node: Optional["BinaryNode"]) -> int:
        res = -1 if node is None else node.height
        return res

    @staticmethod
    def _new_height(node: "BinaryNode") -> int:
        res = max(AVLTree._height(node.left), AVLTree._height(node.right)) + 1
        return res

    @staticmethod
    def _balance(node: "BinaryNode") -> int:
        res = AVLTree._height(node.right) - AVLTree._height(node.left)
        return res

    @staticmethod
    def _small_right_rotation(node: "BinaryNode") -> "BinaryNode":
        if node.left is not None:
            oth_node, node.left = node.left, node.left.right
            oth_node.right = node
            node.height = AVLTree._new_height(node)
            oth_node.height = max(AVLTree._height(oth_node.left), node.height) + 1
            return oth_node
        return node

    @staticmethod
    def _small_left_rotation(node: "BinaryNode") -> "BinaryNode":
        if node.right is not None:
            oth_node, node.right = node.right, node.right.left
            oth_node.left = node
            node.height = AVLTree._new_height(node)
            oth_node.height = max(AVLTree._height(node.right), node.height) + 1
            return oth_node
        return node

    @staticmethod
    def _big_left_rotation(node: "BinaryNode") -> "BinaryNode":
        node.right = AVLTree._small_right_rotation(node.right)
        oth_node = AVLTree._small_left_rotation(node)
        return oth_node

    @staticmethod
    def _big_right_rotation(node: "BinaryNode") -> "BinaryNode":
        node.left = AVLTree._small_left_rotation(node.left)
        oth_node = AVLTree._small_right_rotation(node)
        return oth_node

    @staticmethod
    def _insert(node: Optional["BinaryNode"], value: int) -> "BinaryNode":
        """Вставка значения в узел"""
        if node is None:
            node = BinaryNode(value)
        elif node.value < value:
            node.right = AVLTree._insert(node.right, value)
            if AVLTree._balance(node) == 2:
                if node.right.value < value:
                    node = AVLTree._small_left_rotation(node)
                else:
                    node = AVLTree._big_left_rotation(node)
        elif node.value > value:
            node.left = AVLTree._insert(node.left, value)
            if AVLTree._balance(node) == -2:
                if node.left.value > value:
                    node = AVLTree._small_right_rotation(node)
                else:
                    node = AVLTree._big_right_rotation(node)
        node.height = AVLTree._new_height(node)
        return node

    @staticmethod
    def _min(node: Optional["BinaryNode"]) -> Optional["BinaryNode"]:
        """Поиск минимального значения"""
        if node is None:
            return None
        elif node.left is None:
            return node
        return AVLTree._min(node.left)

    @staticmethod
    def _delete(node: Optional["BinaryNode"], value: int) -> Optional["BinaryNode"]:
        if node is None:
            return None
        elif node.value > value:
            node.left = AVLTree._delete(node.left, value)
        elif node.value < value:
            node.right = AVLTree._delete(node.right, value)
        elif node.left is not None and node.right is not None:
            tmp = AVLTree._min(node.right)
            node.value = tmp.value
            node.right = AVLTree._delete(node.right, node.value)
        else:
            if node.left is None:
                node = node.right
            elif node.right is None:
                node = node.left
        if node is None:
            return None
        node.height = AVLTree._new_height(node)
        if AVLTree._balance(node) == 2:
            if AVLTree._balance(node.right) == 1:
                return AVLTree._small_left_rotation(node)
            return AVLTree._big_left_rotation(node)
        return node

    @staticmethod
    def _prev(node: Optional["BinaryNode"], value: int) -> Union[str, int]:
        """Поиск максимального значения, меньше данного"""
        cur = node
        prev_ = "none"
        while cur is not None:
            if cur.value < value:
                prev_ = cur.value
                cur = cur.right
            else:
                cur = cur.left
        return prev_

    @staticmethod
    def _next(node: Optional["BinaryNode"], value) -> Union[str, int]:
        """Поиск минимального значения, больше данного"""
        cur = node
        next_ = "none"
        while cur is not None:
            if cur.value > value:
                next_ = cur.value
                cur = cur.left
            else:
                cur = cur.right
        return next_

    @staticmethod
    def _exists(node: Optional["BinaryNode"], value: int) -> str:
        """Поиск значения"""
        if node is None:
            return "false"
        elif value < node.value:
            return AVLTree._exists(node.left, value)
        elif value > node.value:
            return AVLTree._exists(node.right, value)
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
    bst = AVLTree()
    for operation in stdin:
        act, val_ = operation.split()
        val = int(val_)
        if act == "insert":
            bst.insert(val)
        elif act == "delete":
            bst.delete(val)
        elif act == "exists":
            res = bst.exists(val)
            stdout.write(f"{res}\n")
        elif act == "prev":
            res = bst.prev(val)
            stdout.write(f"{res}\n")
        elif act == "next":
            res = bst.next(val)
            stdout.write(f"{res}\n")


if __name__ == "__main__":
    main()

