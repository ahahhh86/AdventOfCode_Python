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

    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y)

    def __add__(self, other: "Point|tuple|list") -> "Point":
        match other:
            case Point():
                return Point(self.x + other.x, self.y + other.y)
            case tuple() | list():
                assert len(other) == 2
                return Point(self.x + other[0], self.y + other[1])
            case _:
                raise TypeError(f"Unsupported type: {type(other)}")

    def __sub__(self, other: "Point|tuple|list") -> "Point":
        match other:
            case Point():
                return Point(self.x - other.x, self.y - other.y)
            case tuple() | list():
                assert len(other) == 2
                return Point(self.x - other[0], self.y - other[1])
            case _:
                raise TypeError(f"Unsupported type: {type(other)}")

    def __iter__(self) -> int:
        yield self.x
        yield self.y

    def is_in_bounds(self, min_pos: "Point", max_pos: "Point") -> bool:
        """
        checks if Point is in bounds
        :param min_pos: min bound (included)
        :type min_pos: Point
        :param max_pos: max bound (excluded)
        :type max_pos: Point
        :return: is in bounds
        :rtype: bool
        """
        return min_pos.x <= self.x < max_pos.x and min_pos.y <= self.y < max_pos.y


class Directions:
    NORTH = Point(0, -1)
    NORTH_EAST = Point(1, -1)
    EAST = Point(1, 0)
    SOUTH_EAST = Point(1, 1)
    SOUTH = Point(0, 1)
    SOUTH_WEST = Point(-1, 1)
    WEST = Point(-1, 0)
    NORTH_WEST = Point(-1, -1)

    ADJACENT_4 = (NORTH, EAST, SOUTH, WEST)
    ADJACENT_8 = (NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST)
    CROSS = (NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST)

    @classmethod
    def turn_right_90_deg(cls, direction: Point) -> Point:
        switch = {
            cls.NORTH: cls.EAST,
            cls.EAST: cls.SOUTH,
            cls.SOUTH: cls.WEST,
            cls.WEST: cls.NORTH,
        }
        return switch[direction]

    @classmethod
    def turn_left_90_deg(cls, direction: Point) -> Point:
        switch = {
            cls.NORTH: cls.WEST,
            cls.WEST: cls.SOUTH,
            cls.SOUTH: cls.EAST,
            cls.EAST: cls.NORTH,
        }
        return switch[direction]
