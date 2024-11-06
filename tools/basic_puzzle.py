import itertools
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter_ns

from tools.colors import print_colored, str_colored


@dataclass
class FunctionData:
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
        ns_to_ms = 1_000_000
        return self._time // ns_to_ms


class BasicPuzzle(ABC):
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

    def read_file(self, compile_data: callable(str) = lambda line: line) -> tuple:
        with self._filename.open('r') as file:
            return tuple(
                compile_data(line)
                for line in file.read().splitlines()
            )

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
        if not self._test_function(fn, next(self._test_number), '  Test', self._TEST_COLOR):
            self._failed_tests += 1

    def _end_test(self) -> None:
        if self._failed_tests == 0:
            print_colored('All tests passed', self._PASS_COLOR)
        else:
            print_colored(f'{self._failed_tests} tests failed', self._FAIL_COLOR)
        print()

    def _print_result(self, fn: FunctionData):
        self._test_function(fn, next(self._result_number), 'Part', self._RESULT_COLOR)

    @abstractmethod
    def _test_puzzle(self) -> None:
        pass

    @abstractmethod
    def _solve_puzzle(self) -> None:
        pass

    def solve(self) -> None:
        if __debug__:
            self._start_test()
            self._test_puzzle()
            self._end_test()

        self._solve_puzzle()
