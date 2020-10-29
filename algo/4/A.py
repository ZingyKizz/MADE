from sys import stdin, stdout
from typing import Any


def prnt(*args: Any, sep: str = ' ', end: str = '\n') -> None:
    """Быстрый вывод"""
    stdout.write(sep.join(a.__str__() for a in args) + end)


class Node:
    """Узел"""
    def __init__(self, value: float, masked_value: float = None, next_node: "Node" = None) -> None:
        self.value = value
        self.masked_value = masked_value
        self.next_node = next_node

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"


class Stack:
    """Стэк на основе связного списка"""
    def __init__(self) -> None:
        self.head = None
        self.min_value = None
        self.size = 0

    def is_empty(self) -> bool:
        """Проверка на пустоту"""
        return self.size == 0

    def push(self, value: float) -> None:
        """Добавляет элемент на вершину стэка"""
        self.head = Node(value, self.min_value, self.head)
        self.size += 1
        if self.min_value is None:
            self.min_value = value
        elif value < self.min_value:
            self.min_value = value

    def pop(self) -> None:
        """Удаляет элемент с вершины стэка"""
        if self.is_empty():
            raise IndexError("Can't pop from empty stack")
        self.min_value = self.head.masked_value
        self.head = self.head.next_node
        self.size -= 1

    def get_min(self) -> float:
        """Возвращает минимальный элемент в стэке"""
        if self.is_empty():
            raise IndexError("Can't find minimal value in empty stack")
        return self.min_value

    def get_size(self) -> int:
        """Возвращает текущий размер стэка"""
        return self.size

    def __repr__(self) -> str:
        cur = self.head
        vals = ""
        for i in range(self.size):
            end = "" if i == self.size - 1 else " -> "
            vals += str(cur) + end
            cur = cur.next_node
        return f"{self.__class__.__name__}({vals})"


def main() -> None:
    """Считывание, обработка, вывод"""
    stack = Stack()

    n = int(stdin.readline())
    for _ in range(n):
        inpt = stdin.readline()
        if inpt.startswith("1"):
            _, val = map(int, inpt.split())
            stack.push(val)
        elif inpt.startswith("2"):
            stack.pop()
        elif inpt.startswith("3"):
            min_val = stack.get_min()
            prnt(min_val)


if __name__ == "__main__":
    main()
