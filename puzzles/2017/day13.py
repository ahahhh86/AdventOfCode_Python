"""

"""

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd



class _Scanner:
    def __init__(self, line: str) -> None:
        depth, range_ = line.split(': ')
        self._depth = int(depth)
        self._range = int(range_)
        self._position = 1
        self._pos_increase = True

    def calculate_severity(self):
        return self._depth * self._range

    def move(self):
        if self._pos_increase:
            self._position += 1
            if self._position >= self._range:
                self._pos_increase = False
        else:
            self._position -= 1
            if self._position <= 1:
                self._pos_increase = True

    def is_position_top(self):
        return self._position == 1


def _compile_data(line: str) -> _Scanner:
    return _Scanner(line)


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2017, 1)

    def _test_puzzle(self) -> None:
        pass
        # self._print_test(Fd(3, _sum_digits_part1, ([1, 1, 2, 2],)))

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file_lines(_compile_data)[0]
        # self._print_result(Fd(1182, _sum_digits_part1, (puzzle_input,)))
