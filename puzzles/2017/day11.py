r"""
--- Day 11: Hex Ed ---
Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you,
clearly in distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast,
southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started, you need to determine the fewest
number of steps required to reach him. (A "step" means to move from the hex you are in to any adjacent
hex.)

For example:
    ne,ne,ne is 3 steps away.
    ne,ne,sw,sw is 0 steps away (back where you started).
    ne,ne,s,s is 2 steps away (se,se).
    se,sw,se,sw,sw is 3 steps away (s,s,sw).

Your puzzle answer was 705.

--- Part Two ---
How many steps away is the furthest he ever got from his starting position?

Your puzzle answer was 1469.
"""

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd


def _compile_data(line: str) -> tuple:
    return tuple(i for i in line.split(','))


class _HexGrid:
    def __init__(self, directions: tuple[str, ...]) -> None:
        # https://raw.githubusercontent.com/Hellenic/react-hexgrid/add-typescript-and-storybook/coordinates.png
        self._position = [0, 0, 0]
        self._directions = directions
        self._max_distance = 0

    def move(self) -> int:
        distance = 0
        for direction in self._directions:
            distance = self._move_once(direction)
            if distance > self._max_distance:
                self._max_distance = distance
        return distance

    def get_max_distance(self) -> int:
        return self._max_distance

    def _move_once(self, direction: str) -> int:
        # [+1,-2]: n-s, [+0,-2]: ne-sw, [-0,+1]: nw-se
        match direction:
            case 'n':
                self._position[1] += 1
                self._position[2] -= 1
            case 's':
                self._position[1] -= 1
                self._position[2] += 1

            case 'ne':
                self._position[0] += 1
                self._position[2] -= 1
            case 'sw':
                self._position[0] -= 1
                self._position[2] += 1

            case 'nw':
                self._position[0] -= 1
                self._position[1] += 1
            case 'se':
                self._position[0] += 1
                self._position[1] -= 1

            case _:
                raise ValueError(f"invalid value: {direction}")

        return max(abs(i) for i in self._position)


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2017, 11)

    def _test_puzzle(self) -> None:
        def _test_p1(directions):
            h = _HexGrid(directions)
            return h.move()

        self._print_test(Fd(3, _test_p1, (('ne', 'ne', 'ne'),)))
        self._print_test(Fd(0, _test_p1, (('ne', 'ne', 'sw', 'sw'),)))
        self._print_test(Fd(2, _test_p1, (('ne', 'ne', 's', 's'),)))
        self._print_test(Fd(3, _test_p1, (('se', 'sw', 'se', 'sw', 'sw'),)))

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file(_compile_data)[0]
        h = _HexGrid(puzzle_input)
        self._print_result(Fd(705, h.move, ()))
        self._print_result(Fd(1469, h.get_max_distance, ()))
