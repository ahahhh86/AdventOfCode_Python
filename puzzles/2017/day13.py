"""

"""

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd


class _Scanner:
    def __init__(self, line: str) -> None:
        depth, range_ = line.split(': ')
        self._depth = int(depth)
        self._range = int(range_)
        self.reset_scanner()

    @property
    def depth(self) -> int:
        """depth"""
        return self._depth

    def reset_scanner(self):
        self._position = 1
        self._pos_increase = True

    def calculate_severity(self) -> int:
        return self._depth * self._range

    def move(self) -> None:
        if self._pos_increase:
            self._position += 1
            if self._position >= self._range:
                self._pos_increase = False
        else:
            self._position -= 1
            if self._position <= 1:
                self._pos_increase = True

    def is_position_top(self) -> bool:
        return self._position == 1

    def print(self) -> None:
        """for debugging"""
        print(self._depth, end=" ")
        print(
            # @formatter:off
            *["[ ]" if i != self._position else
            ("[>]" if self._pos_increase else "[<]")
            for i in range(1, self._range + 1)]
            # @formatter:on
        )


class _Scanners:
    def __init__(self, scanners: tuple[_Scanner, ...]) -> None:
        length = max([i.depth for i in scanners]) + 1
        d = {i.depth: i for i in scanners}
        self._scanners: list[_Scanner | None] = [d.get(i, None) for i in range(length)]

    def move(self) -> int:
        def _move_scanners() -> None:
            for s in self._scanners:
                if s:
                    s.move()

        for s in self._scanners:
            if s:
                s.reset_scanner()

        severity = 0
        for scanner in self._scanners:
            if scanner and scanner.is_position_top():
                severity += scanner.calculate_severity()

            _move_scanners()
        return severity

    # TODO: no initial delay, instead send multiple pulses and check, which has no problem
    def move2(self, delay: int = 0) -> bool:
        def _move_scanners() -> None:
            for s in self._scanners:
                if s:
                    s.move()

        for s in self._scanners:
            if s:
                s.reset_scanner()

        for _ in range(delay):
            _move_scanners()

        for scanner in self._scanners:
            if scanner and scanner.is_position_top():
                return False

            _move_scanners()
        return True

    def get_delay(self):
        delay = 0
        while not self.move2(delay):
            delay += 1
        return delay

    # for debugging
    def print(self) -> None:
        """for debugging"""
        for i, v in enumerate(self._scanners):
            if v:
                v.print()
            else:
                print(i, "...")


def _compile_data(line: str) -> _Scanner:
    return _Scanner(line)


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2017, 13)

    def _test_puzzle(self) -> None:
        test_input = tuple(
            map(
                _compile_data,
                (
                    "0: 3",
                    "1: 2",
                    "4: 4",
                    "6: 4",
                )
            )
        )
        scanners = _Scanners(test_input)
        self._print_test(Fd(24, scanners.move, ()))
        self._print_test(Fd(10, scanners.get_delay, ()))

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file_lines(_compile_data)
        scanners = _Scanners(puzzle_input)
        self._print_result(Fd(1960, scanners.move, ()))
        # self._print_result(Fd(1960, scanners.get_delay, ())) # too slow
