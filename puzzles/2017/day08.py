"""
--- Day 8: I Heard You Like Registers ---
You receive a signal directly from the CPU. Because of your recent assistance with jump instructions,
it would like you to compute the result of a series of unusual register instructions.

Each instruction consists of several parts: the register to modify, whether to increase or decrease that
register's value, the amount by which to increase or decrease it, and a condition. If the condition fails,
skip the instruction without modifying the register. The registers all start at 0. The instructions look
like this:
    b inc 5 if a > 1
    a inc 1 if b < 5
    c dec -10 if a >= 1
    c inc -20 if c == 10

These instructions would be processed as follows:
    Because a starts at 0, it is not greater than 1, and so b is not modified.
    a is increased by 1 (to 1) because b is less than 5 (it is 0).
    c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
    c is increased by -20 (to -10) because c is equal to 10.

After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to). However, the CPU doesn't have
the bandwidth to tell you what all the registers are named, and leaves that to you to determine.

What is the largest value in any register after completing the instructions in your puzzle input?

Your puzzle answer was 5102.

--- Part Two ---
To be safe, the CPU also needs to know the highest value held in any register during this process so
that it can decide how much memory to allocate to these operations. For example, in the above instructions,
the highest value ever held was 10 (in register c after the third instruction was evaluated).

Your puzzle answer was 6056.
"""

from collections import defaultdict

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd


class _Instruction:
    def __init__(self, s: str) -> None:
        # pattern: register increase/decrease value 'if' condition_register condition
        buffer = s.split(' ', 5)
        self.register = buffer[0]
        self.increase = buffer[1] == 'inc'
        self.value = int(buffer[2])
        # buffer[3] = 'if' is not used
        self.condition_register = buffer[4]
        self.condition = buffer[5]


class _Registers:
    _DEFAULT_REGISTER = 0

    def __init__(self) -> None:
        self._registers = defaultdict(lambda: self._DEFAULT_REGISTER)
        self._max_register = self._DEFAULT_REGISTER

    def get_highest_register_after_completion(self, instructions: tuple[_Instruction, ...]) -> int:
        """
        :param instructions: instructions how to operate the register
        :type instructions: _Instruction
        :return: the highest number in the register
        :rtype: int
        """
        self._modify_registers(instructions)
        return max(self._registers.values())

    def get_highest_register_during_process(self) -> int:
        """
        :return: the highest value a register held during operations
        :rtype: int
        """
        return self._max_register

    def _modify_registers(self, instructions: tuple[_Instruction, ...]) -> None:
        for i in instructions:
            if eval(f'{self._registers[i.condition_register]} {i.condition}'):
                self._registers[i.register] += i.value if i.increase else -i.value
                self._max_register = max(self._max_register, self._registers[i.register])


def _compile_data(line: str) -> _Instruction:
    return _Instruction(line)


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2017, 8)

    def _test_puzzle(self) -> None:
        def test_register(name: str) -> int:
            return r._registers[name]

        test_input = map(
            _compile_data,
            (
                'b inc 5 if a > 1',
                'a inc 1 if b < 5',
                'c dec -10 if a >= 1',
                'c inc -20 if c == 10',
            )
        )

        r = _Registers()
        self._print_test(Fd(1, r.get_highest_register_after_completion, (test_input,)))
        self._print_test(Fd(1, test_register, ('a',)))
        self._print_test(Fd(0, test_register, ('b',)))
        self._print_test(Fd(-10, test_register, ('c',)))
        self._print_test(Fd(10, r.get_highest_register_during_process, ()))

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file_lines(_compile_data)
        r = _Registers()
        self._print_result(Fd(5102, r.get_highest_register_after_completion, (puzzle_input,)))
        self._print_result(Fd(6056, r.get_highest_register_during_process, ()))
