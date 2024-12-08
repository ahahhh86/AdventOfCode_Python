"""
--- Day 7: Bridge Repair ---
The Historians take you to a familiar rope bridge over a river in the middle of a jungle. The Chief isn't
on this side of the bridge, though; maybe he's on the other side?

When you go to cross the bridge, you notice a group of engineers trying to repair it. (Apparently, it
breaks pretty frequently.) You won't be able to cross until it's fixed.

You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young
elephants were playing nearby and stole all the operators from their calibration equations! They could
finish the calibrations if only someone could determine which test values could possibly be produced
by placing any combination of operators into their calibration equations (your puzzle input).

For example:
    190: 10 19
    3267: 81 40 27
    83: 17 5
    156: 15 6
    7290: 6 8 6 15
    161011: 16 10 13
    192: 17 8 14
    21037: 9 7 18 13
    292: 11 6 16 20

Each line represents a single equation. The test value appears before the colon on each line; it is your
job to determine whether the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers
in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different
types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:
    190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give
29, but choosing * would give the test value (10 * 19 = 190).
    3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators,
two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when
evaluated left-to-right)!
    292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.

The engineers just need the total calibration result, which is the sum of the test values from just the
equations that could possibly be true. In the above example, the sum of the test values for the three
equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?

Your puzzle answer was 1985268524462.

--- Part Two ---
The engineers seem concerned; the total calibration result you gave them is nowhere close to being within
safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type
of operator.

The concatenation operator (||) combines the digits from its left and right inputs into a single number.
For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the
above example has three more equations that can be made true by inserting operators:
    156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
    7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
    192: 17 8 14 can be made true using 17 || 8 + 14.

Adding up all six test values (the three that could be made before using only + and * plus the new three
that can now be made by also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true.
What is their total calibration result?

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
    assert len(operators) + 1 == len(operands)
    result = operands[0]
    for i in range(len(operators)):
        result = _OPERATORS[operators[i]](result, operands[i + 1])
    return result


def _get_correct_value(equation: _Equation) -> int:
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
        results = e.map(_get_correct_value, equations)  # chunksize>1 seems to make the program slower
    return sum(results)


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
        self._print_test(Fd(190, _get_correct_value, (test_input[0],)))
        self._print_test(Fd(3267, _get_correct_value, (test_input[1],)))
        self._print_test(Fd(0, _get_correct_value, (test_input[2],)))
        self._print_test(Fd(0, _get_correct_value, (test_input[3],)))
        self._print_test(Fd(0, _get_correct_value, (test_input[4],)))
        self._print_test(Fd(0, _get_correct_value, (test_input[5],)))
        self._print_test(Fd(0, _get_correct_value, (test_input[6],)))
        self._print_test(Fd(0, _get_correct_value, (test_input[7],)))
        self._print_test(Fd(292, _get_correct_value, (test_input[8],)))
        self._print_test(Fd(3749, _sum_parallel, (test_input,)))

    def _solve_puzzle(self) -> None:
        puzzle_input = list(self.read_file_lines(_compile_data))
        self._print_result(Fd(1985268524462, _sum_parallel, (puzzle_input[:100],)))  # takes a few minutes
