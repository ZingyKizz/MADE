from sys import stdin, stdout
from typing import Any


def prnt(*args: Any, sep: str = ' ', end: str = '\n') -> None:
    """Быстрый вывод"""
    stdout.write(sep.join(a.__str__() for a in args) + end)


class Queue:
    """Очередь на основе циклического саморасширяющегося массива"""
    def __init__(self, capacity: int = 2) -> None:
        self.capacity = capacity
        self.elements = [None] * self.capacity
        self.begin = self.end = 0

    def get_size(self) -> int:
        """Возвращает текущий размер очереди"""
        if self.begin > self.end:
            return self.capacity + self.end - self.begin
        else:
            return self.end - self.begin

    def is_empty(self) -> bool:
        """Проверка на пустоту"""
        return self.get_size() == 0

    def _optimize_capacity(self) -> None:
        """Калибровка вместимости"""
        size = self.get_size()
        capacity = self.capacity
        if size == self.capacity - 1:
            self.capacity *= 2
        elif self.capacity > 4 * size > 0:
            self.capacity //= 2
        else:
            return
        new_elements = [None] * self.capacity
        for i in range(size):
            new_elements[i] = self.elements[(self.begin + i) % capacity]
        self.elements = new_elements
        self.begin = 0
        self.end = size

    def push(self, value: Any) -> None:
        """Добавляет элемент в конец очереди"""
        self._optimize_capacity()
        self.elements[self.end] = value
        self.end = (self.end + 1) % self.capacity

    def pop(self) -> Any:
        """Удаляет элемент из начала очереди"""
        if self.is_empty():
            raise IndexError("Can't pop from empty queue")
        self._optimize_capacity()
        res = self.elements[self.begin]
        self.begin = (self.begin + 1) % self.capacity
        return res

    def __repr__(self) -> str:
        vals = ""
        size = self.get_size()
        for i in range(size):
            end = "" if i == size - 1 else ", "
            vals += str(self.elements[(self.begin + i) % self.capacity]) + end
        return f"{self.__class__.__name__}([{vals}])"


def main() -> None:
    """Считывание, обработка, вывод"""
    queue = Queue()

    n = int(stdin.readline())
    for _ in range(n):
        inpt = stdin.readline()
        if inpt.startswith("+"):
            _, val = inpt.split()
            queue.push(val)
        elif inpt.startswith("-"):
            res = queue.pop()
            prnt(res)


if __name__ == "__main__":
    main()
