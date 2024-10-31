from dataclasses import dataclass
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
        return self._time // 1_000_000



class BasicPuzzle:
    _TEST_COLOR = 'yellow'
    _RESULT_COLOR = 'reset'
    _PASS_COLOR = 'green'
    _FAIL_COLOR = 'red'
    _RESULT_FORMAT = '{:12} | {:>32} | {:>32} | {:>6} ms'
    _TEST_FORMAT = str_colored(
        '  ' + _RESULT_FORMAT,
        _TEST_COLOR
    )

    def __init__(self, year: int, day: int):
        print(f'Year {year:04d} Day {day:02d}')
        self._filename = Path(__file__).parent / Path(f'../input/{year:04d}/day{day:02d}.txt')
        self._tests = []
        self._results = []

    def _read_file_as_lines(self) -> list[str]:
        with self._filename.open('r') as file:
            return file.read().splitlines()

    def _read_file_each_char(self, type_=str) -> list[str]:
        with self._filename.open('r') as file:
            result = []
            for line in file:
                result.extend(type_(char) for char in line.rstrip())
            return result

    def _read_file(self, compile_data: callable(str) = lambda a: a):
        with self._filename.open('r') as file:
            return tuple(
                compile_data(line)
                for line in file.read().splitlines()
            )

    def _add_tests(self, tests: list[FunctionData]):
        if __debug__:
            self._tests.extend(tests)

    def _get_pass_fail(self, value: bool, color: str) -> str:
        if value:
            return str_colored('PASS', self._PASS_COLOR, color)
        else:
            return str_colored('FAIL', self._FAIL_COLOR, color)

    def _print_tests(self):
        def print_test(fn: FunctionData, test_number: int) -> bool:
            with _Timer() as timer:
                result = fn.function(*fn.args)
            success = result == fn.expected
            success_str = self._get_pass_fail(success, self._TEST_COLOR)
            print(
                self._TEST_FORMAT.format(
                    f'Test{test_number:02d}: {success_str}', result, fn.expected, timer.elapsed_ms()
                )
            )
            return success

        if not self._tests:
            return

        print(self._TEST_FORMAT.format(f'Test #', 'result', 'expected', 'time'))
        fail_count = 0
        test: FunctionData
        index = 0
        for test in self._tests:
            if test is None:
                print()
                continue
            index += 1
            if not print_test(test, index):
                fail_count += 1

        if fail_count == 0:
            print_colored('All tests passed', self._PASS_COLOR)
        else:
            print_colored(f'{fail_count} tests failed', self._FAIL_COLOR)
        print()

    def _add_result(self, result: FunctionData) -> None:
        self._results.append(result)

    def _print_results(self) -> None:
        def print_result(fn: FunctionData, result_number: int) -> None:
            with _Timer() as timer:
                result = fn.function(*fn.args)
            success = result == fn.expected
            success_str = self._get_pass_fail(success, self._RESULT_COLOR)
            print(
                self._RESULT_FORMAT.format(
                    f'Part{result_number:02d}: {success_str}', result, fn.expected, timer.elapsed_ms()
                )
            )

        result: FunctionData
        for index, result in enumerate(self._results, 1):
            print_result(result, index)
            # print(f'Part {index}: {result.function(*result.args)}')
        print('\n')

    def solve(self):
        self._print_tests()
        self._print_results()
