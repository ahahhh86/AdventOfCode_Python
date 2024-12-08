"""

"""
import itertools
import math
import winsound
from dataclasses import dataclass
from concurrent import futures

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd


@dataclass
class _Equation:
    result: int
    operands: tuple[int, ...]


def _compile_data(line: str) -> _Equation:
    result, operands = line.split(": ")
    result = int(result)
    assert result > 0
    operands = tuple(int(i) for i in operands.split())
    for i in operands:
        assert i > 0
    return _Equation(result, operands)


_OPERATORS = (
    lambda a, b: a + b,
    lambda a, b: a * b,
)


def _calculate(operands: tuple[int, ...], operators: list):
    # assert len(operators) + 1 == len(operands)
    result = operands[0]
    for i in range(len(operators)):
        result = _OPERATORS[operators[i]](result, operands[i + 1])
    return result


def _get_correct(equation: _Equation) -> int:
    sum_ = sum(equation.operands)
    if equation.result == sum_:
        return equation.result

    prod = math.prod(equation.operands)
    if equation.result == prod:
        return equation.result

    operator_length = len(equation.operands) - 1
    for i in range(1, operator_length):
        operators = (
                tuple(itertools.repeat(1, i)) +
                tuple(itertools.repeat(0, operator_length - i))
        )
        for o in set(itertools.permutations(operators)):
            if equation.result == _calculate(equation.operands, o):
                return equation.result
    return 0

def _sum_parallel(equations: tuple[_Equation, ...]) -> int:
    with futures.ProcessPoolExecutor() as e:
        res = e.map(_get_correct, equations)  # chunksize>1 seems to make the program slower
    return sum(res)


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2024, 7)

    def _test_puzzle(self) -> None:
        test_input = tuple(
            map(
                _compile_data,
                (
                    "190: 10 19",
                    "3267: 81 40 27",
                    "83: 17 5",
                    "156: 15 6",
                    "7290: 6 8 6 15",
                    "161011: 16 10 13",
                    "192: 17 8 14",
                    "21037: 9 7 18 13",
                    "292: 11 6 16 20",
                )

            )
        )
        self._print_test(Fd(190, _get_correct, (test_input[0],)))
        self._print_test(Fd(3267, _get_correct, (test_input[1],)))
        self._print_test(Fd(0, _get_correct, (test_input[2],)))
        self._print_test(Fd(0, _get_correct, (test_input[3],)))
        self._print_test(Fd(0, _get_correct, (test_input[4],)))
        self._print_test(Fd(0, _get_correct, (test_input[5],)))
        self._print_test(Fd(0, _get_correct, (test_input[6],)))
        self._print_test(Fd(0, _get_correct, (test_input[7],)))
        self._print_test(Fd(292, _get_correct, (test_input[8],)))
        self._print_test(Fd(3749, _sum_parallel, (test_input,)))

    def _solve_puzzle(self) -> None:
        puzzle_input = list(self.read_file_lines(_compile_data))
        self._print_result(Fd(1985268524462, _sum_parallel, (puzzle_input,)))
        winsound.Beep(666, 750)
