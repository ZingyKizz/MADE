import sys
from io import IOBase, BytesIO
from os import read, write, fstat
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

    @classmethod
    def from_coords(cls, x: float, y: float):
        """Initialize from coordinates"""
        return Vector(Point(0, 0), Point(x, y))

    def __mul__(self, other: "Vector") -> float:
        """Dot product"""
        return self.x * other.x + self.y * other.y

    def __neg__(self) -> "Vector":
        """Unary minus"""
        return Vector.from_coords(-self.x, -self.y)

    def cross_product(self, other: "Vector") -> float:
        """Cross product"""
        return self.x * other.y - self.y * other.x

    def __repr__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}({self.x}, {self.y})"


class Segment:
    """Segment"""
    def __init__(self, left: "Point", right: "Point") -> None:
        """Initialize from two points"""
        self.left = left
        self.right = right

    def __contains__(self, point: "Point") -> bool:
        """Check if point contains to segment"""
        vector1 = Vector(point, self.left)
        vector2 = Vector(point, self.right)
        return (
            vector1.cross_product(vector2) == 0
            and vector1 * vector2 <= 0
        )

    def intersects(self, other: "Segment") -> bool:
        """Check if segment intersects with another"""
        a, b = self.left, self.right
        c, d = other.left, other.right

        ab = Vector(a, b)
        ac = Vector(a, c)
        ca = -ac
        ad = Vector(a, d)
        cd = Vector(c, d)
        cb = Vector(c, b)

        ab_x_ac = ab.cross_product(ac)
        ab_x_ad = ab.cross_product(ad)
        cd_x_ca = cd.cross_product(ca)
        cd_x_cb = cd.cross_product(cb)

        if not (ab_x_ac or ab_x_ad or cd_x_ca or cd_x_cb):
            if (
                c in self
                or d in self
                or a in other
                or b in other
            ):
                return True
            else:
                return False
        return (
            ab_x_ac * ab_x_ad <= 0
            and cd_x_ca * cd_x_cb <= 0
        )

    def __repr__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}({self.left}, {self.right})"


def main() -> None:
    """Input, processing, output"""
    x1, y1, x2, y2 = map(int, split_input())
    x3, y3, x4, y4 = map(int, split_input())
    segment1 = Segment(Point(x1, y1), Point(x2, y2))
    segment2 = Segment(Point(x3, y3), Point(x4, y4))
    fast_print("YES" if segment1.intersects(segment2) else "NO")


if __name__ == "__main__":
    main()
