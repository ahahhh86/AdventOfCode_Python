"""
Contains the base class for all puzzles
"""

import itertools
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter_ns

from tools.colors import print_colored, str_colored


@dataclass
class FunctionData:
    """
    dataclass to transport functions and results for testing
    """
    expected: int | str
    function: callable
    args: tuple


class _Timer:
    def __enter__(self) -> '_Timer':
        self._time = perf_counter_ns()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._time = perf_counter_ns() - self._time

    def elapsed_ms(self) -> int:
        """
        :return: time since timer was started
        :rtype: int in ms
        """
        ns_to_ms = 1_000_000
        return self._time // ns_to_ms


class BasicPuzzle(ABC):
    """
    basic class for all puzzles
    includes functions to read input from file and print results on the screen
    """
    _TEST_COLOR = 'yellow'
    _RESULT_COLOR = 'reset'
    _PASS_COLOR = 'green'
    _FAIL_COLOR = 'red'
    _RESULT_FORMAT = '{:14} | {:>32} | {:>32} | {:>6} ms'

    def __init__(self, year: int, day: int):
        print(f'Year {year:04d} Day {day:02d}')
        self._filename = Path(__file__).parent / Path(f'../input/{year:04d}/day{day:02d}.txt')
        self._test_number = itertools.count(1)
        self._failed_tests = 0
        self._result_number = itertools.count(1)

    def read_file_lines(self, compile_data: callable = lambda line: line) -> tuple:
        """
        reads all lines from input file and converts the data in each line according to compile_data
        :param compile_data: convert each line into usable data
        :type compile_data: callable
        :return: tuple with an item for each line
        :rtype: tuple depending on compile_data
        """
        with self._filename.open('r') as file:
            return tuple(
                compile_data(line)
                for line in file.read().splitlines()
            )

    def read_file(self, compile_data: callable = lambda s: s):
        """
        reads the whole file (striping trailing whitespace) converting the data according to compile_data
        :param compile_data: converts the file into usable data
        :type compile_data: callable
        :return: depending on compile_data
        :rtype: depending on compile_data
        """
        with self._filename.open('r') as file:
            return compile_data(file.read().rstrip())

    @classmethod
    def _test_function(cls, fn: FunctionData, number: int, start_str: str, color: str) -> bool:
        def _get_pass_fail(value: bool) -> str:
            return (
                str_colored('PASS', cls._PASS_COLOR, color)
                if value else
                str_colored('FAIL', cls._FAIL_COLOR, color)
            )

        with _Timer() as timer:
            result = fn.function(*fn.args)
        success = result == fn.expected
        success_str = _get_pass_fail(success)

        print(
            str_colored(
                cls._RESULT_FORMAT.format(
                    f'{start_str}{number:02d}: {success_str}',
                    result, fn.expected, timer.elapsed_ms(),
                ),
                color
            )
        )
        return success

    @classmethod
    def _start_test(cls) -> None:
        print_colored(
            cls._RESULT_FORMAT.format(f'  Test #', 'result', 'expected', 'time'),
            cls._TEST_COLOR
        )

    def _print_test(self, fn: FunctionData) -> None:
        """
        print the result of a test
        :param fn: data and expected output of the test
        :type fn: FunctionData
        :return: None
        :rtype: None
        """
        if not self._test_function(fn, next(self._test_number), '  Test', self._TEST_COLOR):
            self._failed_tests += 1

    def _end_test(self) -> None:
        if self._failed_tests == 0:
            print_colored('All tests passed', self._PASS_COLOR)
        else:
            print_colored(f'{self._failed_tests} tests failed', self._FAIL_COLOR)
        print()

    def _print_result(self, fn: FunctionData) -> None:
        """
        print the solution of the puzzle, expected output is used to check if refactoring worked
        :param fn: data of the function containing the result
        :type fn: FunctionData
        :return: None
        :rtype: None
        """
        self._test_function(fn, next(self._result_number), 'Part', self._RESULT_COLOR)

    @abstractmethod
    def _test_puzzle(self) -> None:
        """
        Abstract method to test if the puzzle works
        """
        pass

    @abstractmethod
    def _solve_puzzle(self) -> None:
        """
        Abstract method to solve the puzzle
        """
        pass

    def solve(self) -> None:
        """
        solves the puzzle
        :return: None
        :rtype: None
        """
        if __debug__:
            self._start_test()
            self._test_puzzle()
            self._end_test()

        self._solve_puzzle()
