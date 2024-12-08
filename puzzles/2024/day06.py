"""
--- Day 6: Guard Gallivant ---
The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype
suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very
convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518
while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the
lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...

The map shows the current position of the guard with ^ (to indicate the guard is currently facing up
from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown
as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:
    If there is something directly in front of you, turn right 90 degrees.
    Otherwise, take a step forward.

Following the above protocol, the guard moves up several times until she reaches an obstacle (in this
case, a pile of failed suit prototypes):
    ....#.....
    ....^....#
    ..........
    ..#.......
    .......#..
    ..........
    .#........
    ........#.
    #.........
    ......#...

Because there is now an obstacle in front of the guard, she turns right before continuing straight in
her new facing direction:
    ....#.....
    ........>#
    ..........
    ..#.......
    .......#..
    ..........
    .#........
    ........#.
    #.........
    ......#...

Reaching another obstacle (a spool of several very long polymers), she turns right again and continues
downward:
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#......v.
    ........#.
    #.........
    ......#...

This process continues for a while, but the guard eventually leaves the mapped area (after walking past
a tank of universal solvent):
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#........
    ........#.
    #.........
    ......#v..

By predicting the guard's route, you can determine which specific positions in the lab will be in the
patrol path. Including the guard's starting position, the positions visited by the guard before leaving
the area are marked with an X:
    ....#.....
    ....XXXXX#
    ....X...X.
    ..#.X...X.
    ..XXXXX#X.
    ..X.X.X.X.
    .#XXXXXXX.
    .XXXXXXX#.
    #XXXXXXX..
    ......#X..

In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped
area?

Your puzzle answer was 5153.

--- Part Two ---
While The Historians begin working around the guard's patrol route, you borrow their fancy device and
step outside the lab. From the safety of a supply closet, you time travel through the last few months
and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol
area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd
like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest
of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible
positions for such an obstruction. The new obstruction can't be placed at the guard's starting position
- the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard
to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to
show a position where the guard moves up/down, - to show a position where the guard moves left/right,
and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:
    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ....|..#|.
    ....|...|.
    .#.O^---+.
    ........#.
    #.........
    ......#...

Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:
    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    ......O.#.
    #.........
    ......#...

Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom
right quadrant:
    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    .+----+O#.
    #+----+...
    ......#...

Option four, put an alchemical retroencabulator near the bottom left corner:
    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    ..|...|.#.
    #O+---+...
    ......#...

Option five, put the alchemical retroencabulator a bit to the right instead:
    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    ....|.|.#.
    #..O+-+...
    ......#...

Option six, put a tank of sovereign glue right next to the tank of universal solvent:
    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    .+----++#.
    #+----++..
    ......#O..

It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can
put it into position without the guard noticing. The important thing is having enough options that you
can find one that minimizes time paradoxes, and in this example, there are 6 different positions you
could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions
could you choose for this obstruction?

Your puzzle answer was 1711.
"""

from copy import deepcopy

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd
from tools.point import Directions, Point


class _LabArea:
    class _Guard:
        # The example and my puzzle input are both north, so it is the default atm
        def __init__(self, position: Point, direction: Point = Directions.NORTH) -> None:
            self.position = position
            self.direction = direction

        def turn(self) -> None:
            self.direction = Directions.turn_right_90_deg(self.direction)

        def tuple(self) -> tuple[Point, Point]:
            return self.position, self.direction


    _OBSTRUCTION = "#"
    _PATH = "."

    def __init__(self, area: list[str, ...]) -> None:
        self._area = [list(s) for s in area]
        self._area_size = Point(len(area), len(area[0]))
        for i in self._area:
            assert len(i) == self._area_size.y

        self._guard_start = self._create_guard()
        self._steps = {self._guard_start.position}

    def calculate_when_guard_left(self):
        guard = deepcopy(self._guard_start)
        while pos := self._move_once(guard):
            self._steps.add(pos[0])
        return len(self._steps)

    def count_loops(self):
        loop_counter = 0
        for obstruction in self._steps:
            if self._area[obstruction.y][obstruction.x] != self._PATH:
                continue
            self._area[obstruction.y][obstruction.x] = self._OBSTRUCTION
            if self._is_guard_looping():
                loop_counter += 1
            self._area[obstruction.y][obstruction.x] = self._PATH
        return loop_counter

    def _is_guard_looping(self) -> bool:
        guard = deepcopy(self._guard_start)
        steps = {guard.tuple()}
        while step := self._move_once(guard):
            if step in steps:
                return True
            steps.add(step)
        return False

    def _create_guard(self) -> _Guard:
        for i in range(self._area_size.x):
            for j in range(self._area_size.y):
                if self._area[i][j] not in (self._OBSTRUCTION, self._PATH):
                    return self._Guard(Point(j, i))

    def _move_once(self, guard: _Guard) -> tuple[Point, Point] | None:
        new_position = guard.position + guard.direction
        if not new_position.is_in_bounds(Point(0, 0), self._area_size):
            return None
        if self._area[new_position.y][new_position.x] != self._OBSTRUCTION:
            guard.position = new_position
        else:
            guard.turn()
        return guard.tuple()


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2024, 6)

    def _test_puzzle(self) -> None:
        test_input = ("""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""".splitlines())
        area = _LabArea(test_input)
        self._print_test(Fd(41, area.calculate_when_guard_left, ()))
        self._print_test(Fd(6, area.count_loops, ()))

    def _solve_puzzle(self) -> None:
        puzzle_input = list(self.read_file_lines())
        area = _LabArea(puzzle_input)
        self._print_result(Fd(5153, area.calculate_when_guard_left, ()))
        # self._print_result(Fd(1711, area.count_loops, ()))  # slow for me ~25s, TODO pake parallel
