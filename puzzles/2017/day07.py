"""
--- Day 7: Recursive Circus ---
Wandering further through the circuits of the computer, you come upon a tower of programs that have gotten
themselves into a bit of trouble. A recursive algorithm has gotten out of hand, and now they're balanced
precariously in a large tower.

One program at the bottom supports the entire tower. It's holding a large disc, and on the disc are balanced
several more sub-towers. At the bottom of these sub-towers, standing on the bottom disc, are other programs,
each holding their own disc, and so on. At the very tops of these sub-sub-sub-...-towers, many programs
stand simply keeping the disc below them balanced but with no disc of their own.

You offer to help, but first you need to understand the structure of these towers. You ask each program
to yell out their name, their weight, and (if they're holding a disc) the names of the programs immediately
above them balancing on that disc. You write this information down (your puzzle input). Unfortunately,
in their panic, they don't do this in an orderly fashion; by the time you're done, you're not sure which
program gave which information.

For example, if your list is the following:
    pbga (66)
    xhth (57)
    ebii (61)
    havc (66)
    ktlj (57)
    fwft (72) -> ktlj, cntj, xhth
    qoyq (66)
    padx (45) -> pbga, havc, qoyq
    tknk (41) -> ugml, padx, fwft
    jptl (61)
    ugml (68) -> gyxo, ebii, jptl
    gyxo (61)
    cntj (57)

...then you would be able to recreate the structure of the towers that looks like this:

                gyxo
              /
         ugml - ebii
       /      \
      |         jptl
      |
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |
      |         ktlj
       \      /
         fwft - cntj
              \
                xhth

In this example, tknk is at the bottom of the tower (the bottom program), and is holding up ugml, padx,
and fwft. Those programs are, in turn, holding up other programs; in this example, none of those programs
are holding up any other programs, and are all the tops of their own towers. (The actual tower balancing
in front of you is much larger.)

Before you're ready to help them, you need to make sure your information is correct. What is the name
of the bottom program?

Your puzzle answer was hlqnsbe.

--- Part Two ---
The programs explain the situation: they can't get down. Rather, they could get down, if they weren't
expending all of their energy trying to keep the tower balanced. Apparently, one program has the wrong
weight, and until it's fixed, they're stuck here.

For any program holding a disc, each program standing on that disc forms a sub-tower. Each of those sub-towers
are supposed to be the same weight, or the disc itself isn't balanced. The weight of a tower is the sum
of the weights of the programs in that tower.

In the example above, this means that for ugml's disc to be balanced, gyxo, ebii, and jptl must all have
the same weight, and they do: 61.

However, for tknk to be balanced, each of the programs standing on its disc and all programs above it
must each match. This means that the following sums must all be the same:
    ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
    padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
    fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243

As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the other two. Even though the
nodes above ugml are balanced, ugml itself is too heavy: it needs to be 8 units lighter for its stack
to weigh 243 and keep the towers balanced. If this change were made, its weight would be 60.

Given that exactly one program is the wrong weight, what would its weight need to be to balance the entire
tower?

Your puzzle answer was 1993.
"""

import re
from dataclasses import dataclass

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd


@dataclass
class _Tower:
    name: str
    own_weight: int
    children: list
    parent: str = ''
    total_weight: int = None

    _INPUT_PATTERN = re.compile(r'(\w+) \((\d+)\)(?: -> (.+))?')

    def __str__(self) -> str:
        return f'{self.name} -> {self.own_weight} / {self.total_weight} -> {self.children}'

    @classmethod
    def create_tower(cls, s: str) -> "_Tower":
        # pattern: name weight -> children
        matcher = re.match(cls._INPUT_PATTERN, s)
        name, weight = matcher.groups()[:2]
        children = matcher.group(3).split(', ') if matcher.group(3) else ()
        return cls(name, int(weight), children)


class _Towers:
    def __init__(self, towers: list[_Tower] | tuple[_Tower, ...]) -> None:
        self._towers = {t.name: t for t in towers}
        self._first_parent = None

    def find_first_parent(self) -> str:
        self._add_parents()
        tower = next(iter(self._towers.values()))
        while tower.parent:
            tower = self._towers[tower.parent]
        self._first_parent = tower.name
        return tower.name

    def adjust_unbalanced(self):
        name = self._find_unbalanced()
        children = [self._towers[n] for n in self._towers[name].children]
        children.sort(key=lambda t: t.total_weight)
        if children[0].total_weight == children[1].total_weight:
            difference = children[0].total_weight - children[-1].total_weight
            adjusted_weight = children[-1].own_weight + difference
        else:
            difference = children[-1].total_weight - children[0].total_weight
            adjusted_weight = children[0].own_weight + difference
        return adjusted_weight

    def _add_parents(self) -> None:
        for tower in self._towers.values():
            for child in tower.children:
                self._towers[child].parent = tower.name

    def _calculate_total_weight(self, name: str = None) -> int:
        if name is None:
            if self._first_parent == '':
                self.find_first_parent()
            name = self._first_parent

        tower = self._towers[name]
        if tower.total_weight is None:
            tower.total_weight = (
                    tower.own_weight +
                    (
                        sum([self._calculate_total_weight(n) for n in tower.children])
                        if tower.children else
                        0
                    )
            )

        return tower.total_weight

    def _find_unbalanced(self) -> str:
        def are_children_balanced(children: list[str]) -> bool:
            default = self._towers[children[0]].total_weight
            return all(self._towers[name].total_weight == default for name in children)

        self._calculate_total_weight()
        for tower in self._towers.values():
            if tower.children and not are_children_balanced(tower.children):
                return tower.name
        raise AssertionError("No matching tower")


def _compile_data(line: str) -> _Tower:
    return _Tower.create_tower(line)


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2017, 7)

    def _test_puzzle(self) -> None:
        puzzle_test = list(
            map(
                _compile_data,
                [
                    'pbga (66)',
                    'xhth (57)',
                    'ebii (61)',
                    'havc (66)',
                    'ktlj (57)',
                    'fwft (72) -> ktlj, cntj, xhth',
                    'qoyq (66)',
                    'padx (45) -> pbga, havc, qoyq',
                    'tknk (41) -> ugml, padx, fwft',
                    'jptl (61)',
                    'ugml (68) -> gyxo, ebii, jptl',
                    'gyxo (61)',
                    'cntj (57)',
                ]
            )
        )
        t = _Towers(puzzle_test)
        self._print_test(Fd('tknk', t.find_first_parent, ()))
        print()

        # noinspection PyProtectedMember
        self._print_test(Fd(251, t._calculate_total_weight, ('ugml',)))
        # noinspection PyProtectedMember
        self._print_test(Fd(243, t._calculate_total_weight, ('padx',)))
        # noinspection PyProtectedMember
        self._print_test(Fd(243, t._calculate_total_weight, ('fwft',)))
        # noinspection PyProtectedMember
        self._print_test(Fd(2 * 243 + 251 + 41, t._calculate_total_weight, ('tknk',)))
        print()
        # noinspection PyProtectedMember
        self._print_test(Fd('tknk', t._find_unbalanced, ()))
        self._print_test(Fd(60, t.adjust_unbalanced, ()))

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file(_compile_data)
        t = _Towers(puzzle_input)
        self._print_result(Fd('hlqnsbe', t.find_first_parent, ()))
        self._print_result(Fd(1993, t.adjust_unbalanced, ()))
