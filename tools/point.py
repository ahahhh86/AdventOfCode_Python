"""
Module containing a (two-dimensional) pint
"""
from dataclasses import dataclass


#frozen to make hashable
@dataclass(frozen=True)
class Point:
    """
    class that represents a two-dimensional point
    you can add two points or add a tuple or list with two elements
    """
    x: int
    y: int

    def __abs__(self) -> int:
        return abs(self.x) + abs(self.y)

    def __str__(self) -> str:
        return f'x: {self.x}, y: {self.y}'

    def __add__(self, other: "Point|tuple|list") -> "Point":
        match other:
            case Point():
                return Point(self.x + other.x, self.y + other.y)
            case tuple() | list():
                assert len(other) == 2
                return Point(self.x + other[0], self.y + other[1])
            case _:
                raise TypeError(f"Unsupported type: {type(other)}")

    def __iter__(self) -> int:
        yield self.x
        yield self.y
