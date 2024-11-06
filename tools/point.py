from dataclasses import dataclass


#frozen to make hashable
@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'

    def __add__(self, other: "Point|tuple"):
        match other:
            case Point():
                return Point(self.x + other.x, self.y + other.y)
            case tuple():
                return Point(self.x + other[0], self.y + other[1])

    def __iter__(self):
        yield self.x
        yield self.y
