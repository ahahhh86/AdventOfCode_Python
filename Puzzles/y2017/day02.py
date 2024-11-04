"""
--- Day 2: Corruption Checksum ---
As you walk through the door, a glowing humanoid shape yells in your direction. "You there! Your state
appears to be idle. Come help us repair the corruption in this spreadsheet - if we take another millisecond,
we'll have to display an hourglass cursor!"

The spreadsheet consists of rows of apparently-random numbers. To make sure the recovery process is on
the right track, they need you to calculate the spreadsheet's checksum. For each row, determine the difference
between the largest value and the smallest value; the checksum is the sum of all of these differences.

For example, given the following spreadsheet:
    5 1 9 5
    7 5 3
    2 4 6 8

    The first row's largest and smallest values are 9 and 1, and their difference is 8.
    The second row's largest and smallest values are 7 and 3, and their difference is 4.
    The third row's difference is 6.

In this example, the spreadsheet's checksum would be 8 + 4 + 6 = 18.

What is the checksum for the spreadsheet in your puzzle input?

Your puzzle answer was 45351.

--- Part Two ---
"Great work; looks like we're on the right track after all. Here's a star for your effort." However,
the program seems a little worried. Can programs be worried?

"Based on what we're seeing, it looks like all the User wanted is some information about the evenly divisible
values in the spreadsheet. Unfortunately, none of us are equipped for that kind of calculation - most
of us specialize in bitwise operations."

It sounds like the goal is to find the only two numbers in each row where one evenly divides the other
- that is, where the result of the division operation is a whole number. They would like you to find
those numbers on each line, divide them, and add up each line's result.

For example, given the following spreadsheet:
    5 9 2 8
    9 4 7 3
    3 8 6 5

    In the first row, the only two numbers that evenly divide are 8 and 2; the result of this division is 4.
    In the second row, the two numbers are 9 and 3; the result is 3.
    In the third row, the result is 2.

In this example, the sum of the results would be 4 + 3 + 2 = 9.

What is the sum of each row's result in your puzzle input?

Your puzzle answer was 275.
"""

from tools.basic_puzzle import BasicPuzzle
from tools.basic_puzzle import FunctionData as Fd



def _compile_data(line: str) -> tuple[int, ...]:
    return tuple(int(i) for i in line.split())



def _calculate_checksum(value: list[list[int]]) -> int:
    result = 0
    for line in value:
        difference = max(line) - min(line)
        result += difference
    return result



def _calculate_checksum2(value: list[list[int]]) -> int:
    result = 0
    for line in value:
        dividable = []
        for i in line:
            for j in line:
                if i != j and i % j == 0:
                    dividable.append(i // j)
        result += sum(dividable)
    return result



class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2017, 2)

        test_input1 = map(
            _compile_data,
            [
                '5 1 9 5',
                '7 5 3',
                '2 4 6 8',
            ]
        )
        test_input2 = map(
            _compile_data,
            [
                '5 9 2 8',
                '9 4 7 3',
                '3 8 6 5',
            ]
        )
        puzzle_input = self._read_file(_compile_data)

        self._add_tests(
            [
                Fd(18, _calculate_checksum, (test_input1,)),
                Fd(9, _calculate_checksum2, (test_input2,)),
            ]
        )

        self._add_result(Fd(45351, _calculate_checksum, (puzzle_input,)))
        self._add_result(Fd(275, _calculate_checksum2, (puzzle_input,)))
