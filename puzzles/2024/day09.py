"""

"""

from copy import deepcopy
from dataclasses import dataclass

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd


@dataclass
class _SingleFileLayout:
    id: int
    length: int
    free_space: int

    def __str__(self):
        return str(self.id) * self.length + "." * self.free_space


def _compile_data(line: str) -> list[_SingleFileLayout]:
    assert len(line) % 2 == 1
    result = []
    disk_map = (int(i) for i in line)
    index = 0
    while True:
        length = next(disk_map)
        try:
            free_space = next(disk_map)
        except StopIteration:
            result.append(_SingleFileLayout(index, length, 0))
            break

        result.append(_SingleFileLayout(index, length, free_space))
        index += 1
    return result


class _DataMap:
    _EMPTY_SPACE = "."

    def __init__(self, files: list[_SingleFileLayout]) -> None:
        self._files = files

    def calculate_checksum_part1(self) -> int:
        return self._calculate_checksum(self._move_blocks_part1())

    def calculate_checksum_part2(self) -> int:
        return self._calculate_checksum(self._move_blocks_part2())

    @classmethod
    def _create_blocks(cls, files: list[_SingleFileLayout]) -> list[str | int]:
        result: list[str | int] = []
        for file in files:
            result.extend([file.id] * file.length)
            result.extend(cls._EMPTY_SPACE * file.free_space)
        return result

    def _move_blocks_part1(self) -> list[str | int]:
        blocks = self._create_blocks(self._files)
        used_diskspace = len([c for c in blocks if c != self._EMPTY_SPACE])
        j = 1  # 0 can not be empty space

        for i in range(len(blocks) - 1, used_diskspace - 1, -1):
            if blocks[i] == self._EMPTY_SPACE:
                continue
            while blocks[j] != self._EMPTY_SPACE:
                j += 1
            blocks[j], blocks[i] = blocks[i], blocks[j]
        return blocks

    def _move_blocks_part2(self) -> list[str | int]:
        blocks = deepcopy(self._files)
        i = len(blocks) - 1
        while i > 0:
            for j in range(i):
                if blocks[i].length <= blocks[j].free_space:
                    blocks.insert(j + 1, block := blocks.pop(i))

                    # after inserting blocks[i] is the one before the one moved
                    blocks[i].free_space += block.length + block.free_space
                    block.free_space = blocks[j].free_space - block.length
                    blocks[j].free_space = 0
                    break
            else:
                i -= 1

        return self._create_blocks(blocks)

    @classmethod
    def _calculate_checksum(cls, blocks) -> int:
        return sum(i * v for i, v in enumerate(blocks) if v != cls._EMPTY_SPACE)


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2024, 9)

    def _test_puzzle(self) -> None:
        m1 = _DataMap(_compile_data("12345"))
        self._print_test(Fd(60, m1.calculate_checksum_part1, ()))

        m2 = _DataMap(_compile_data("2333133121414131402"))
        self._print_test(Fd(1928, m2.calculate_checksum_part1, ()))
        self._print_test(Fd(2858, m2.calculate_checksum_part2, ()))

        print()

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file(_compile_data)
        m = _DataMap(puzzle_input)
        self._print_result(Fd(6360094256423, m.calculate_checksum_part1, ()))
        # TODO: why does it not work with puzzle input but with test input?
        self._print_result(Fd(0000000000000, m.calculate_checksum_part2, ()))  # 6379637944410 too low
