from dataclasses import dataclass
from itertools import count
from pathlib import Path
from time import perf_counter_ns

from tools.colors import print_colored, str_colored



@dataclass
class FunctionData:
    expected: int
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



class BasicPuzzle:
    _TEST_COLOR = 'yellow'
    _RESULT_COLOR = 'reset'
    _PASS_COLOR = 'green'
    _FAIL_COLOR = 'red'
    _RESULT_FORMAT = '{:14} | {:>32} | {:>32} | {:>6} ms'

    def __init__(self, year: int, day: int):
        print(f'Year {year:04d} Day {day:02d}')
        self._filename = Path(__file__).parent / Path(f'../input/{year:04d}/day{day:02d}.txt')
        self._tests = []
        self._results = []

    def read_file(self, compile_data: callable(str) = lambda line: line) -> tuple:
        with self._filename.open('r') as file:
            return tuple(
                compile_data(line)
                for line in file.read().splitlines()
            )

    def add_tests(self, tests: list[FunctionData]):
        if __debug__:
            self._tests.extend(tests)

    def add_result(self, result: FunctionData) -> None:
        self._results.append(result)

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

    def _print_tests(self) -> None:
        if not self._tests:
            return

        print_colored(
            self._RESULT_FORMAT.format(f'  Test #', 'result', 'expected', 'time'),
            self._TEST_COLOR
        )

        fail_count = 0
        index = count(1)
        test: FunctionData
        for test in self._tests:
            if test is None:
                print()
            elif not self._test_function(test, next(index), '  Test', self._TEST_COLOR):
                fail_count += 1

        if fail_count == 0:
            print_colored('All tests passed', self._PASS_COLOR)
        else:
            print_colored(f'{fail_count} tests failed', self._FAIL_COLOR)
        print()

    def _print_results(self) -> None:
        result: FunctionData
        index = count(1)
        for result in self._results:
            self._test_function(result, next(index), 'Part', self._RESULT_COLOR)
        print('\n')

    def solve(self) -> None:
        self._print_tests()
        self._print_results()
