"""
--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only
button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd
like to know if you could help her with her word search (your puzzle input). She only has to find one
word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping
other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you
need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been
replaced with .:
    ..X...
    .SAMX.
    .A..A.
    XMAS.S
    .X....

The actual word search will be full of letters instead. For example:
    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX

In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters
not involved in any XMAS have been replaced with .:
    ....XXMAS.
    .SAMXMS...
    ...S..A...
    ..A.A.MS.X
    XMASAMX.MM
    X.....XA.A
    S.S.S.S.SS
    .A.A.A.A.A
    ..M.M.M.MM
    .X.X.XMASX

Take a look at the little Elf's word search. How many times does XMAS appear?

Your puzzle answer was 2633.

--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS
puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to
achieve that is like this:
    M.S
    .A.
    M.S

Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can
be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:
    .M.S......
    ..A..MSMS.
    .M.S.MAA..
    ..A.ASMSM.
    .M.S.M....
    ..........
    S.S.S.S.S.
    .A.A.A.A..
    M.M.M.M.M.
    ..........

In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many
times does an X-MAS appear?

Your puzzle answer was 1936.
"""

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd
from tools.point import Point


def _compile_data(line: str) -> tuple[str, ...]:
    return tuple(line)


class _Matrix:
    _WORD_DIRECTIONS = (
        Point(-1, -1), Point(0, -1), Point(1, -1),
        Point(-1, 0), Point(1, 0),  # (0, 0) is excluded
        Point(-1, 1), Point(0, 1), Point(1, 1),
    )
    _CROSS_DIRECTIONS = (
        Point(-1, -1), Point(1, -1),
        Point(-1, 1), Point(1, 1),
    )
    _WORD = "XMAS"
    _WORD_LENGTH = len(_WORD)
    _CROSS = "MAS"

    def __init__(self, matrix: tuple[tuple[str, ...], ...]):
        self._matrix = matrix
        self._matrix_size = Point(len(self._matrix), len(self._matrix[0]))
        for i in self._matrix:
            assert len(i) == self._matrix_size.y

    def count_words(self) -> int:
        found = 0
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[i])):
                for direction in self._WORD_DIRECTIONS:
                    found += self._is_word(Point(i, j), direction)
        return found

    def count_cross(self) -> int:
        found = 0
        for i in range(1, len(self._matrix) - 1):
            for j in range(1, len(self._matrix[i]) - 1):
                found += self._is_cross(Point(i, j))
        return found

    def _is_word(self, pos: Point, direction: Point, index: int = 0) -> bool:
        # if not in bound return False
        # do not use try: -1 would be a valid index
        if not (0 <= pos.x < self._matrix_size.x and 0 <= pos.y < self._matrix_size.y):
            return False

        value = self._matrix[pos.x][pos.y]
        if value != self._WORD[index]:
            return False

        if index + 1 >= self._WORD_LENGTH:
            return value == self._WORD[index]

        return self._is_word(pos + direction, direction, index + 1)

    def _is_cross(self, pos: Point) -> bool:
        # skip first and last line, because pos should be in the center of the X
        if not (0 < pos.x < self._matrix_size.x - 1 and 0 < pos.y < self._matrix_size.y - 1):
            return False

        if self._matrix[pos.x][pos.y] != self._CROSS[1]:
            return False

        corners_pos = [pos + p for p in self._CROSS_DIRECTIONS]
        corners = [self._matrix[p.x][p.y] for p in corners_pos]

        # this may not work with all words, but works with "MAS"
        assert len(self._CROSS) == 3
        assert self._CROSS[0] != self._CROSS[2]

        for i in corners:
            if i not in (self._CROSS[0], self._CROSS[2]):
                return False
        return corners[0] != corners[3] and corners[1] != corners[2]


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2024, 4)

    def _test_puzzle(self) -> None:
        test_input = tuple(
            map(
                _compile_data,
                (
                    "MMMSXXMASM",
                    "MSAMXMSMSA",
                    "AMXSXMAAMM",
                    "MSAMASMSMX",
                    "XMASAMXAMM",
                    "XXAMMXXAMA",
                    "SMSMSASXSS",
                    "SAXAMASAAA",
                    "MAMMMXMMMM",
                    "MXMXAXMASX",
                )
            )
        )
        matrix = _Matrix(test_input)
        self._print_test(Fd(18, matrix.count_words, ()))
        self._print_test(Fd(9, matrix.count_cross, ()))

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file_lines(_compile_data)
        matrix = _Matrix(puzzle_input)
        self._print_result(Fd(2633, matrix.count_words, ()))
        self._print_result(Fd(1936, matrix.count_cross, ()))
