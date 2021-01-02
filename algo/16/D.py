import sys
from io import IOBase, BytesIO
from os import read, write, fstat
from math import atan2
#################################################################################
"""Fast input/output"""

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


def _input():
    return stdin.readline().rstrip()


def split_input():
    return _input().split()


def fast_print(*args, sep=" ", end="\n"):
    for a in args:
        stdout.write(f"{a}{sep}")
    stdout.write(f"{end}")
#################################################################################


class Point:
    """Point"""
    def __init__(self, x: float, y: float) -> None:
        """Initialize from coordinates"""
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}({self.x}, {self.y})"


class Vector:
    """Vector"""
    def __init__(self, start: "Point", end: "Point") -> None:
        """Initialize from two points"""
        self.x = end.x - start.x
        self.y = end.y - start.y

    def __mul__(self, other: "Vector") -> float:
        """Dot product"""
        return self.x * other.x + self.y * other.y

    def cross_product(self, other: "Vector") -> float:
        """Cross product"""
        return self.x * other.y - self.y * other.x

    def angle(self, other: "Vector") -> float:
        """Angle between vectors in radians"""
        return atan2(self.cross_product(other), self * other)

    def __repr__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}({self.x}, {self.y})"


class Segment:
    """Segment"""
    def __init__(self, left: "Point", right: "Point") -> None:
        """Initialize from two points"""
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}({self.left}, {self.right})"


class Polygon:
    """Polygon"""
    def __init__(self, *points: "Point"):
        """Initialize from list of points"""
        self.number_of_points = len(points)
        self.sides = [Segment(points[i], points[(i + 1) % self.number_of_points]) for i in range(self.number_of_points)]
        self.points = points

    def __repr__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}({', '.join(map(repr, self.sides))})"

    def square(self) -> float:
        """Square of polygon"""
        res = 0
        p0 = self.points[0]
        for i in range(1, self.number_of_points - 1):
            vector1 = Vector(p0, self.points[i])
            vector2 = Vector(p0, self.points[i + 1])
            res += vector1.cross_product(vector2)
        return abs(res / 2)


def main() -> None:
    """Input, processing, output"""
    number_of_points = int(_input())
    polygon_points = []
    for _ in range(number_of_points):
        x, y = map(int, split_input())
        polygon_points.append(Point(x, y))
    polygon = Polygon(*polygon_points)
    square = polygon.square()
    fast_print(square)


if __name__ == "__main__":
    main()
