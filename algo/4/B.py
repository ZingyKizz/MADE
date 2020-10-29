from sys import stdin, stdout
from typing import Any


def prnt(*args: Any, sep: str = ' ', end: str = '\n') -> None:
    """Быстрый вывод"""
    stdout.write(sep.join(a.__str__() for a in args) + end)


class Stack:
    """Стэк на основе саморасширяющегося массива"""
    def __init__(self, capacity: int = 2) -> None:
        self.size = 0
        self.capacity = capacity
        self.elements = [None] * self.capacity

    def __getitem__(self, item: int) -> Any:
        if item >= self.size:
            raise IndexError("Stack index out of range")
        return self.elements[item]

    def is_empty(self) -> bool:
        """Проверка на пустоту"""
        return self.size == 0

    def _optimize_capacity(self) -> None:
        """Калибровка вместимости"""
        if self.size == self.capacity - 1:
            self.capacity *= 2
        elif self.capacity > 4 * self.size > 0:
            self.capacity //= 2
        else:
            return
        new_elements = [None] * self.capacity
        for i in range(self.size):
            new_elements[i] = self.elements[i]
        self.elements = new_elements

    def push(self, value: Any) -> None:
        """Добавляет элемент на вершину стэка"""
        self._optimize_capacity()
        self.elements[self.size] = value
        self.size += 1

    def pop(self) -> Any:
        """Удаляет элемент с вершины стэка"""
        if self.is_empty():
            raise IndexError("Can't pop from empty stack")
        self._optimize_capacity()
        self.size -= 1
        return self.elements[self.size]

    def get_size(self) -> int:
        """Возвращает текущий размер стэка"""
        return self.size

    def __repr__(self) -> str:
        vals = ", ".join(str(elem) for elem in self.elements if elem is not None)
        return f"{self.__class__.__name__}([{vals}])"


def main() -> None:
    """Считывание, обработка, вывод"""
    stack = Stack()

    for s in stdin.readline().split():
        if s.isdigit():
            stack.push(s)
        else:
            b, a = stack.pop(), stack.pop()
            res = eval(f"{a}{s}{b}")
            stack.push(res)
    res = stack.pop()
    prnt(res)


if __name__ == "__main__":
    main()
