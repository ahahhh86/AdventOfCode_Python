"""
--- Day 8: Resonant Collinearity ---
You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise,
it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter
Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned
to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create
a map (your puzzle input) of these antennas. For example:
    ............
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ............
    ............
    ........A...
    .........A..
    ............
    ............

The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies
of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas
of the same frequency - but only when one of the antennas is twice as far away as the other. This means
that for any pair of antennas with the same frequency, there are two antinodes, one on either side of
them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:
    ..........
    ...#......
    ..........
    ....a.....
    ..........
    .....a....
    ..........
    ......#...
    ..........
    ..........

Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four
antinodes, but two are off the right side of the map, so instead it adds only two:
    ..........
    ...#......
    #.........
    ....a.....
    ........a.
    .....a....
    ..#.......
    ......#...
    ..........
    ..........

Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However,
antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency
capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:
    ..........
    ...#......
    #.........
    ....a.....
    ........a.
    .....a....
    ..#.......
    ......A...
    ..........
    ..........

The first example has antennas with two different frequencies, so the antinodes they create look like
this, plus an antinode overlapping the topmost A-frequency antenna:
    ......#....#
    ...#....0...
    ....#0....#.
    ..#....0....
    ....0....#..
    .#....A.....
    ...#........
    #......#....
    ........A...
    .........A..
    ..........#.
    ..........#.

Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique
locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an
antinode?

Your puzzle answer was 278.

--- Part Two ---
Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant
harmonics into your calculations.

Whoops!

After updating your model, it turns out that an antinode occurs at any grid position exactly in line
with at least two antennas of the same frequency, regardless of distance. This means that some of the
new antinodes will occur at the position of each antenna (unless that antenna is the only one of its
frequency).

So, these three T-frequency antennas now create many antinodes:
    T....#....
    ...T......
    .T....#...
    .........#
    ..#.......
    ..........
    ...#......
    ..........
    ....#.....
    ..........

In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also
antinodes! This brings the total number of antinodes in the above example to 9.

The original example now has 34 antinodes, including the antinodes that appear on every antenna:
    ##....#....#
    .#.#....0...
    ..#.#0....#.
    ..##...0....
    ....0....#..
    .#...#A....#
    ...#..#.....
    #....#.#....
    ..#.....A...
    ....#....A..
    .#........#.
    ...#......##

Calculate the impact of the signal using this updated model. How many unique locations within the bounds
of the map contain an antinode?

Your puzzle answer was 1067.
"""


from collections import defaultdict

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd
from tools.point import Point


class _Map:
    _EMPTY_POSITION = "."

    def __init__(self, map: tuple[str, ...]) -> None:
        self._map_size = Point(len(map[0]), len(map))
        for i in map:
            assert len(i) == self._map_size.x

        self._antennas = defaultdict(list[Point])
        for i in range(self._map_size.y):
            for j in range(self._map_size.x):
                value = map[i][j]
                if value != self._EMPTY_POSITION:
                    self._antennas[value].append(Point(j, i))

        for i in self._antennas.values():
            assert len(i) > 1

        self._antinodes = set()

    def calculate_antinodes_part1(self) -> int:
        return self._sum_antinodes(self._calculate_antinode_pair_part1)

    def calculate_antinodes_part2(self) -> int:
        return self._sum_antinodes(self._calculate_antinodes_part2)

    def _calculate_antinode_pair_part1(self, a: Point, b: Point) -> tuple[Point, ...]:
        difference = b - a
        antinodes = a - difference, b + difference
        return tuple(a for a in antinodes if a.is_in_bounds(Point(0, 0), self._map_size))

    def _calculate_antinodes_part2(self, a: Point, b: Point) -> tuple[Point, ...]:
        def _add_antinodes(start: Point, rel_position: Point) -> tuple[Point, ...]:
            nodes = [start]
            node = start + rel_position
            while node.is_in_bounds(Point(0, 0), self._map_size):
                nodes.append(node)
                node += rel_position
            return tuple(nodes)

        difference = b - a
        return _add_antinodes(a, -difference) + _add_antinodes(b, difference)

    def _calculate_antinodes_per_frequency(self, antennas: list[Point], fn: callable):
        length = len(antennas)
        for i in range(length - 1):
            for j in range(i + 1, length):
                pair = fn(antennas[i], antennas[j])
                for p in pair:
                    self._antinodes.add(p)

    def _sum_antinodes(self, fn: callable):
        for positions in self._antennas.values():
            self._calculate_antinodes_per_frequency(positions, fn)
        return len(self._antinodes)


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2024, 8)

    def _test_puzzle(self) -> None:
        test_input = (
            "............",
            "........0...",
            ".....0......",
            ".......0....",
            "....0.......",
            "......A.....",
            "............",
            "............",
            "........A...",
            ".........A..",
            "............",
            "............",
        )
        m = _Map(test_input)
        self._print_test(Fd(14, m.calculate_antinodes_part1, ()))
        self._print_test(Fd(34, m.calculate_antinodes_part2, ()))

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file_lines()
        m = _Map(puzzle_input)
        self._print_result(Fd(278, m.calculate_antinodes_part1, ()))
        self._print_result(Fd(1067, m.calculate_antinodes_part2, ()))
