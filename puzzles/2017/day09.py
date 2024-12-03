"""
--- Day 9: Stream Processing ---
A large stream blocks your path. According to the locals, it's not safe to cross the stream at the moment
because it's full of garbage. You look down at the stream; rather than water, you discover that it's
a stream of characters.

You sit for a while and record part of the stream (your puzzle input). The characters represent groups
- sequences that begin with { and end with }. Within a group, there are zero or more other things, separated
by commas: either another group or garbage. Since groups can contain other groups, a } only closes the
most-recently-opened unclosed group - that is, they are nestable. Your puzzle input represents a single,
large group which itself contains many smaller ones.

Sometimes, instead of a group, you will find garbage. Garbage begins with < and ends with >. Between
those angle brackets, almost any character can appear, including { and }. Within garbage, < has no special
meaning.

In a futile attempt to clean up the garbage, some program has canceled some of the characters within
it using !: inside garbage, any character that comes after ! should be ignored, including <, >, and even
another !.

You don't see any characters that deviate from these rules. Outside garbage, you only find well-formed
groups, and garbage always terminates according to the rules above.

Here are some self-contained pieces of garbage:
    <>, empty garbage.
    <random characters>, garbage containing random characters.
    <<<<>, because the extra < are ignored.
    <{!>}>, because the first > is canceled.
    <!!>, because the second ! is canceled, allowing the > to terminate the garbage.
    <!!!>>, because the second ! and the first > are canceled.
    <{o"i!a,<{i<a>, which ends at the first >.

Here are some examples of whole streams and the number of groups they contain:
    {}, 1 group.
    {{{}}}, 3 groups.
    {{},{}}, also 3 groups.
    {{{},{},{{}}}}, 6 groups.
    {<{},{},{{}}>}, 1 group (which itself contains garbage).
    {<a>,<a>,<a>,<a>}, 1 group.
    {{<a>},{<a>},{<a>},{<a>}}, 5 groups.
    {{<!>},{<!>},{<!>},{<a>}}, 2 groups (since all but the last > are canceled).

Your goal is to find the total score for all groups in your input. Each group is assigned a score which
is one more than the score of the group that immediately contains it. (The outermost group gets a score
of 1.)
    {}, score of 1.
    {{{}}}, score of 1 + 2 + 3 = 6.
    {{},{}}, score of 1 + 2 + 2 = 5.
    {{{},{},{{}}}}, score of 1 + 2 + 3 + 3 + 3 + 4 = 16.
    {<a>,<a>,<a>,<a>}, score of 1.
    {{<ab>},{<ab>},{<ab>},{<ab>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
    {{<!!>},{<!!>},{<!!>},{<!!>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
    {{<a!>},{<a!>},{<a!>},{<ab>}}, score of 1 + 2 = 3.

What is the total score for all groups in your input?

Your puzzle answer was 7616.

--- Part Two ---
Now, you're ready to remove the garbage.

To prove you've removed it, you need to count all of the characters within the garbage. The leading and
trailing < and > don't count, nor do any canceled characters or the ! doing the canceling.
    <>, 0 characters.
    <random characters>, 17 characters.
    <<<<>, 3 characters.
    <{!>}>, 2 characters.
    <!!>, 0 characters.
    <!!!>>, 0 characters.
    <{o"i!a,<{i<a>, 10 characters.

How many non-canceled characters are within the garbage in your puzzle input?

Your puzzle answer was 3838.
"""

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd


class _Stream:
    _MARKED_GARBAGE = ''
    _CANCEL_NEXT = '!'
    _START_GARBAGE = '<'
    _END_GARBAGE = '>'
    _START_GROUP = '{'
    _END_GROUP = '}'

    def __init__(self, stream: list[str]) -> None:
        self._stream = list(stream)

    def calculate_score(self) -> int:
        """
        :return: score for all groups
        :rtype: int
        """
        self._remove_canceled()
        self._remove_garbage()
        score = 0
        level = 0
        for char in self._stream:
            if char == self._START_GROUP:
                level += 1
            elif char == self._END_GROUP:
                score += level
                level -= 1
        assert level == 0  # not all groups were closed
        return score

    def count_garbage(self) -> int:
        """
        :return: number of non-canceled characters within the garbage
        :rtype: int
        """
        return sum(self._MARKED_GARBAGE == char for char in self._stream)

    def _remove_canceled(self) -> None:
        i = 0
        while i < len(self._stream):
            if self._stream[i] == self._CANCEL_NEXT:
                del self._stream[i]
                del self._stream[i]  # del after !
                # because of del: no i += 1 needed
            else:
                i += 1

    def _remove_garbage(self) -> None:
        length = len(self._stream)
        i = 0
        while i < length:
            if self._stream[i] == self._START_GARBAGE:
                i += 1
                while i < length:
                    if self._stream[i] == self._END_GARBAGE:
                        break
                    self._stream[i] = self._MARKED_GARBAGE
                    i += 1
            i += 1


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2017, 9)

    def _test_puzzle(self) -> None:
        def test_part1(s: list[str]) -> int:
            stream = _Stream(s)
            return stream.calculate_score()

        def test_part2(s: list[str]) -> int:
            stream = _Stream(s)
            stream.calculate_score()
            return stream.count_garbage()

        self._print_test(Fd(1, test_part1, (list('{}'),)))
        self._print_test(Fd(6, test_part1, (list('{{{}}}'),)))
        self._print_test(Fd(5, test_part1, (list('{{},{}}'),)))
        self._print_test(Fd(16, test_part1, (list('{{{},{},{{}}}}'),)))
        self._print_test(Fd(1, test_part1, (list('{<a>,<a>,<a>,<a>}'),)))
        self._print_test(Fd(9, test_part1, (list('{{<ab>},{<ab>},{<ab>},{<ab>}}'),)))
        self._print_test(Fd(9, test_part1, (list('{{<!!>},{<!!>},{<!!>},{<!!>}}'),)))
        self._print_test(Fd(3, test_part1, (list('{{<a!>},{<a!>},{<a!>},{<ab>}}'),)))
        print()
        self._print_test(Fd(0, test_part2, (list('<>'),)))
        self._print_test(Fd(17, test_part2, (list('<random characters>'),)))
        self._print_test(Fd(3, test_part2, (list('<<<<>'),)))
        self._print_test(Fd(2, test_part2, (list('<{!>}>'),)))
        self._print_test(Fd(0, test_part2, (list('<!!>'),)))
        self._print_test(Fd(0, test_part2, (list('<!!!>>'),)))
        self._print_test(Fd(10, test_part2, (list('<{o"i!a,<{i<a>'),)))
        print()
        self._print_test(Fd(4, test_part2, (list('{<a>,<a>,<a>,<a>}'),)))
        self._print_test(Fd(8, test_part2, (list('{{<ab>},{<ab>},{<ab>},{<ab>}}'),)))
        self._print_test(Fd(0, test_part2, (list('{{<!!>},{<!!>},{<!!>},{<!!>}}'),)))
        self._print_test(Fd(17, test_part2, (list('{{<a!>},{<a!>},{<a!>},{<ab>}}'),)))

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file(lambda line: list(line))
        stream = _Stream(puzzle_input)
        self._print_result(Fd(7616, stream.calculate_score, ()))
        self._print_result(Fd(3838, stream.count_garbage, ()))
