"""
"""
from tools.basic_puzzle import BasicPuzzle
from tools.basic_puzzle import FunctionData as Fd




def _compile_data(line: str) -> int:
    return int(line)



class _Spiral:
    _RIGHT = 'right'
    _LEFT = 'left'
    _UP = 'top'
    _DOWN = 'down'

    def __init__(self, field_count: int) -> None:
        self._field_count = field_count
        self._fields = {(0, 0): 1}
        self._position = [0, 0]
        self._create_spiral()

    @classmethod
    def _get_direction(cls):
        while True:
            yield cls._RIGHT
            yield cls._UP
            yield cls._LEFT
            yield cls._DOWN

    @staticmethod
    def _get_steps():
        counter = 0
        while True:
            counter += 1
            yield counter
            yield counter

    def _create_spiral(self) -> None:
        direction_generator = self._get_direction()
        steps_generator = self._get_steps()
        count = 1
        while True:
            direction = next(direction_generator)
            steps = next(steps_generator)

            for _ in range(steps):
                if count >= self._field_count:
                    return
                count += 1
                self._next_pos(direction)

    def _next_pos(self, direction: str):
        match direction:
            case self._RIGHT:
                self._position[0] += 1
            case self._LEFT:
                self._position[0] -= 1
            case self._UP:
                self._position[1] -= 1
            case self._DOWN:
                self._position[1] += 1
        self._fields[tuple(self._position)] = 0

    def get_distance(self):
        return abs(self._position[0]) + abs(self._position[1])



class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        def test(i: int):
            s = _Spiral(i)
            return s.get_distance()

        super().__init__(2017, 3)
        puzzle_input = self._read_file(_compile_data)[0]

        self._add_tests(
            [
                Fd(0, test, (1,)),
                Fd(3, test, (12,)),
                Fd(2, test, (23,)),
                Fd(31, test, (1024,)),
            ]
        )

        sp = _Spiral(puzzle_input)
        self._add_result(Fd(480, _Spiral.get_distance, (sp,)))
        # self._add_result(Fd(1152, _sum_digits_part2, (puzzle_input,)))
