"""
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting
up while spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

While this is very space-efficient (no squares are skipped), requested data must be carried back to square
1 (the location of the only access port for this memory system) by programs that can only move up, down,
left, or right. They always take the shortest path: the Manhattan Distance between the location of the
data and square 1.

For example:
    Data from square 1 is carried 0 steps, since it's at the access port.
    Data from square 12 is carried 3 steps, such as: down, left, left.
    Data from square 23 is carried only 2 steps: up twice.
    Data from square 1024 must be carried 31 steps.

How many steps are required to carry the data from the square identified in your puzzle input all the
way to the access port?

Your puzzle answer was 480.

--- Part Two ---
As a stress test on the system, the programs here clear the grid and then store the value 1 in square
1. Then, in the same allocation order as shown above, they store the sum of the values in all adjacent
squares, including diagonals.

So, the first few squares' values are chosen as follows:
    Square 1 starts with the value 1.
    Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
    Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
    Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
    Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.

Once a square is written, its value does not change. Therefore, the first few squares would receive the
following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...

What is the first value written that is larger than your puzzle input?

Your puzzle answer was 349975.
"""

from typing import Generator

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd
from tools.point import Point


class _Spiral:
    _RIGHT = 'right'
    _LEFT = 'left'
    _UP = 'top'
    _DOWN = 'down'
    _START_POS = Point(0, 0)
    _INVALID_SUM = -1
    _ADJACENT_POSITIONS = (
        Point(-1, -1), Point(0, -1), Point(1, -1),
        Point(-1, 0), Point(1, 0),  # (0, 0) is excluded
        Point(-1, 1), Point(0, 1), Point(1, 1),
    )


    class _DirectionGenerator:
        def __init__(self) -> None:
            def _generate() -> Generator[str, None, None]:
                while True:
                    yield _Spiral._RIGHT
                    yield _Spiral._UP
                    yield _Spiral._LEFT
                    yield _Spiral._DOWN

            self._generator = _generate()

        def __call__(self) -> str:
            return next(self._generator)


    class _StepGenerator:
        def __init__(self) -> None:
            def _generate() -> Generator[int, None, None]:
                counter = 1
                while True:
                    yield counter
                    yield counter
                    counter += 1

            self._generator = _generate()

        def __call__(self) -> int:
            return next(self._generator)


    def __init__(self, field_count: int) -> None:
        self._field_count = field_count
        self._fields = {self._START_POS: 1}
        self._position = self._START_POS
        self._min_larger_sum = self._INVALID_SUM  # minimum sum that is larger than field_count

    def get_distance(self) -> int:
        self._create_spiral()
        return abs(self._position)

    def min_larger_sum(self) -> int:
        if self._min_larger_sum == self._INVALID_SUM:
            self._create_spiral()
        return self._min_larger_sum

    def _create_spiral(self) -> None:
        def set_next_position(d: str) -> None:
            match d:
                case self._RIGHT:
                    self._position += (+1, 0)
                case self._LEFT:
                    self._position += (-1, 0)
                case self._UP:
                    self._position += (0, -1)
                case self._DOWN:
                    self._position += (0, +1)

        def add_sum_of_adjacent() -> None:
            # we do not need any more sums after we found one big enough
            # makes the program a lot faster
            if self._min_larger_sum != self._INVALID_SUM:
                return
            adjacent_sum = 0
            for pos in self._ADJACENT_POSITIONS:
                try:
                    adjacent_sum += self._fields[self._position + pos]
                except KeyError:
                    pass  # if field does not exist, do not add anything
            # noinspection PyTypeChecker
            # Expected type 'tuple[int, int]', got 'tuple[int, ...]' instead
            self._fields[self._position] = adjacent_sum
            if adjacent_sum >= self._field_count:
                self._min_larger_sum = adjacent_sum

        generate_direction = self._DirectionGenerator()
        generate_steps = self._StepGenerator()
        count = 1

        # loop over the directions right, up, left, down, right, ...
        while True:
            direction = generate_direction()
            steps = generate_steps()

            # loop over each step in one direction
            for _ in range(steps):
                if count >= self._field_count:
                    return
                count += 1
                set_next_position(direction)
                add_sum_of_adjacent()


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2017, 3)

    def _test_puzzle(self) -> None:
        def test_spiral_distance(i: int) -> int:
            spiral = _Spiral(i)
            return spiral.get_distance()

        def test_spiral_sum(i: int) -> int:
            spiral = _Spiral(i)
            return spiral.min_larger_sum()

        self._print_test(Fd(0, test_spiral_distance, (1,)))
        self._print_test(Fd(3, test_spiral_distance, (12,)))
        self._print_test(Fd(2, test_spiral_distance, (23,)))
        self._print_test(Fd(31, test_spiral_distance, (1024,)))
        print()
        # Tests 1 to 3 will fail even if the spiral creation works fine
        # self._print_test(Fd(1, test_spiral_sum, (1,)))  # no need to create the spiral => no sum returned
        # self._print_test(Fd(1, test_spiral_sum, (2,)))  # all sums < 2
        # self._print_test(Fd(2, test_spiral_sum, (3,)))  # all sums < 3
        self._print_test(Fd(4, test_spiral_sum, (4,)))
        self._print_test(Fd(5, test_spiral_sum, (5,)))

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file(lambda line: int(line))[0]
        spiral = _Spiral(puzzle_input)
        self._print_result(Fd(480, _Spiral.get_distance, (spiral,)))
        self._print_result(Fd(349975, _Spiral.min_larger_sum, (spiral,)))
