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
    Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values,
4.
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

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd
from typing import Generator



def _compile_data(line: str) -> int:
    return int(line)



class _Spiral:
    _RIGHT = 'right'
    _LEFT = 'left'
    _UP = 'top'
    _DOWN = 'down'



    class _DirectionGenerator:
        def __init__(self) -> None:
            self._generator = self._get_direction()

        def __call__(self) -> str:
            return next(self._generator)

        @staticmethod
        def _get_direction() -> Generator[str, None, None]:
            while True:
                yield _Spiral._RIGHT
                yield _Spiral._UP
                yield _Spiral._LEFT
                yield _Spiral._DOWN



    class _StepGenerator:
        def __init__(self) -> None:
            self._generator = self._get_steps()

        def __call__(self) -> int:
            return next(self._generator)

        @staticmethod
        def _get_steps() -> Generator[int, None, None]:
            counter = 0
            while True:
                counter += 1
                yield counter
                yield counter



    def __init__(self, field_count: int) -> None:
        self._field_count = field_count
        self._fields = {(0, 0): 1}
        self._position = [0, 0]
        self._last_sum = -1
        self._create_spiral()

    def _create_spiral(self) -> None:
        generate_directions = self._DirectionGenerator()
        generate_steps = self._StepGenerator()
        count = 1
        while True:
            direction = generate_directions()
            steps = generate_steps()

            for _ in range(steps):
                if count >= self._field_count:
                    return
                count += 1
                sum_ = self._next_pos(direction)
                if self._last_sum < 0 and sum_ >= self._field_count:
                    self._last_sum = sum_

    def _next_pos(self, direction: str) -> int:
        match direction:
            case self._RIGHT:
                self._position[0] += 1
            case self._LEFT:
                self._position[0] -= 1
            case self._UP:
                self._position[1] -= 1
            case self._DOWN:
                self._position[1] += 1
        return self._add_sum_of_adjacent()

    def get_distance(self) -> int:
        return abs(self._position[0]) + abs(self._position[1])

    def _add_sum_of_adjacent(self) -> int:
        pos = tuple(self._position)
        sum_ = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                try:
                    sum_ += self._fields[pos[0] + i, pos[1] + j]
                except KeyError:
                    pass
        self._fields[pos] = sum_
        return sum_

    def get_last_sum(self):
        return self._last_sum



class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        def test_part1(i: int):
            s = _Spiral(i)
            return s.get_distance()

        def test_part2(i: int):
            s = _Spiral(i)
            return s.get_last_sum()

        super().__init__(2017, 3)
        puzzle_input = self._read_file(_compile_data)[0]

        self._add_tests(
            [
                Fd(0, test_part1, (1,)),
                Fd(3, test_part1, (12,)),
                Fd(2, test_part1, (23,)),
                Fd(31, test_part1, (1024,)),
                None,
                Fd(1, test_part2, (1,)),
                Fd(1, test_part2, (2,)),
                Fd(2, test_part2, (3,)),
                Fd(4, test_part2, (4,)),
                Fd(5, test_part2, (5,)),
            ]
        )

        sp = _Spiral(puzzle_input)
        self._add_result(Fd(480, _Spiral.get_distance, (sp,)))
        self._add_result(Fd(349975, _Spiral.get_last_sum, (sp,)))
