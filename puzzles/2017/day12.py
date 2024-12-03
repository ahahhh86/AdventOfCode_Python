"""
--- Day 12: Digital Plumber ---
Walking along the memory banks of the stream, you find a small village that is experiencing a little
confusion: some programs can't communicate with each other.

Programs in this village communicate using a fixed system of pipes. Messages are passed between programs
using these pipes, but most programs aren't connected to each other directly. Instead, programs pass
messages between each other until the message reaches the intended recipient.

For some reason, though, some of these messages aren't ever reaching their intended recipient, and the
programs suspect that some pipes are missing. They would like you to investigate.

You walk through the village and record the ID of each program and the IDs with which it can communicate
directly (your puzzle input). Each program has one or more programs with which it can communicate, and
these pipes are bidirectional; if 8 says it can communicate with 11, then 11 will say it can communicate
with 8.

You need to figure out how many programs are in the group that contains program ID 0.

For example, suppose you go door-to-door like a travelling salesman and record the following list:
    0 <-> 2
    1 <-> 1
    2 <-> 0, 3, 4
    3 <-> 2, 4
    4 <-> 2, 3, 6
    5 <-> 6
    6 <-> 4, 5

In this example, the following programs are in the group that contains program ID 0:
    Program 0 by definition.
    Program 2, directly connected to program 0.
    Program 3 via program 2.
    Program 4 via program 2.
    Program 5 via programs 6, then 4, then 2.
    Program 6 via programs 4, then 2.

Therefore, a total of 6 programs are in this group; all but program 1, which has a pipe that connects
it to itself.

How many programs are in the group that contains program ID 0?

Your puzzle answer was 141.

--- Part Two ---
There are more programs than just the ones in the group containing program ID 0. The rest of them have
no way of reaching that group, and still might have no way of reaching each other.

A group is a collection of programs that can all communicate via pipes either directly or indirectly.
The programs you identified just a moment ago are all part of the same group. Now, they would like you
to determine the total number of groups.

In the example above, there were 2 groups: one consisting of programs 0,2,3,4,5,6, and the other consisting
solely of program 1.

How many groups are there in total?

Your puzzle answer was 171.
"""

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd


def _compile_data(line: str) -> tuple[int, ...]:
    connections = line.split(' <-> ')[1]
    return tuple(int(i) for i in connections.split(', '))

def _group_connections(connections: tuple, group: set, index: int) -> None:
    for connection in connections[index]:
        if connection not in group:
            group.add(connection)
            _group_connections(connections, group, connection)


def _count_connections(connections: tuple[int, ...]) -> int:
    group = {0}
    _group_connections(connections, group, 0)
    return len(group)

def _count_groups(connections: tuple[int, ...]) -> int:
    groups = set()
    for i in range(len(connections)):
        # do not need to test each index, you could skip it, if it is already in a group
        # but when I tried this, it got slower not faster
        group = {i}
        _group_connections(connections, group, i)
        groups.add(frozenset(group))
    return len(groups)


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2017, 12)

    def _test_puzzle(self) -> None:
        test_input = tuple(
            map(
                _compile_data,
                (
                    "0 <-> 2",
                    "1 <-> 1",
                    "2 <-> 0, 3, 4",
                    "3 <-> 2, 4",
                    "4 <-> 2, 3, 6",
                    "5 <-> 6",
                    "6 <-> 4, 5",
                )
            )
        )
        self._print_test(Fd(6, _count_connections, (test_input,)))

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file_lines(_compile_data)
        self._print_result(Fd(141, _count_connections, (puzzle_input,)))
        self._print_result(Fd(171, _count_groups, (puzzle_input,)))
