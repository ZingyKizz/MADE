from sys import stdin, stdout
from typing import Any, Union


def prnt(*args: Any, sep: str = ' ', end: str = '\n') -> None:
    """Быстрый вывод"""
    stdout.write(sep.join(a.__str__() for a in args) + end)


class Heap:
    """Приоритетная очередь на основе бинарной кучи"""
    def __init__(self):
        self.elements = []
        self.size = 0

    def is_empty(self) -> bool:
        """Проверка на пустоту"""
        return self.size == 0

    def _swap(self, i: int, j: int) -> None:
        """"Меняет местами два элемента кучи с индексами i и j"""
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]

    def _siftup(self, idx: int) -> None:
        """Просеивание вверх из вершины с индексом idx"""
        while self.elements[idx] < self.elements[(idx - 1) // 2] and idx > 0:
            self._swap(idx, (idx - 1) // 2)
            idx = (idx - 1) // 2

    def _siftdown(self, idx: int) -> None:
        """Просеивание вниз из вершины с индексом idx"""
        while 2 * idx + 1 < self.size:
            cur = self.elements[idx]
            left = self.elements[2 * idx + 1]
            right = self.elements[2 * idx + 2] if 2 * idx + 2 != self.size else (float('inf'), float('inf'))
            if cur <= left and cur <= right:
                return
            else:
                small_child_idx = 2 * idx + 1 if left <= right else 2 * idx + 2
                self._swap(idx, small_child_idx)
                idx = small_child_idx

    def push(self, value: float, action_id: int) -> None:
        """Добавление элемента в кучу"""
        elem = (value, action_id)
        self.elements.append(elem)
        self.size += 1
        self._siftup(self.size - 1)

    def pop(self) -> Union[str, float]:
        """Удаление элемента из кучи"""
        if self.is_empty():
            return '*'
        self._swap(0, self.size - 1)
        res = self.elements.pop()
        self.size -= 1
        self._siftdown(0)
        return res

    def _find_index(self, action_id: int) -> Union[int, None]:
        """Поиск индекса элемента по action_id"""
        for idx, elem in enumerate(self.elements):
            val, act = elem
            if act == action_id:
                return idx
        return None

    def decrease_key(self, value: float, action_id: int) -> None:
        """Уменьшение элемента до значения value, добавленном на шаге action_id"""
        idx = self._find_index(action_id)
        if idx is None:
            return
        elem = (value, action_id)
        self.elements[idx] = elem
        self._siftup(idx)

    def __repr__(self) -> str:
        vals = ", ".join(map(str, self.elements))
        return f"{self.__class__.__name__}([{vals}])"


def main() -> None:
    """Считывание, обработка, вывод"""
    heap = Heap()

    for act_id, action in enumerate(stdin, 1):
        if action.startswith("push"):
            _, val = action.split()
            heap.push(int(val), act_id)
        elif action.startswith("extract-min"):
            res = heap.pop()
            prnt(*res)
        elif action.startswith("decrease-key"):
            _, act_id_, val = action.split()
            heap.decrease_key(int(val), int(act_id_))


if __name__ == '__main__':
    main()
