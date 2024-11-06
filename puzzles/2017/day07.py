"""

"""
import re

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd
from dataclasses import dataclass

@dataclass
class _Tower:
    name: str
    weight: int
    children: list
    parent: str

    _INPUT_PATTERN = re.compile(r'(\w+) \((\d+)\)(?: -> (.+))?')

    def __str__(self):
        return f'{self.parent} -> {self.name} {self.weight} -> {self.children}'

    @classmethod
    def create_tower(cls, s: str) -> "_Tower":
        #pattern: name weight -> above
        matcher = re.match(cls._INPUT_PATTERN, s)
        name, weight = matcher.groups()[:2]
        above = matcher.group(3).split(', ') if matcher.group(3) else ()  # TODO: include in _INPUT_PATTERN
        return cls(name, int(weight), above, '')

class _Towers:
    def __init__(self, towers: list|tuple):
        self._towers = {t.name: t for t in towers}

    def _add_parents(self) -> None:
        tower: _Tower
        for tower in self._towers.values():
            for child in tower.children:
                self._towers[child].parent = tower.name

    def find_first_parent(self) -> str:
        self._add_parents()
        tower = next(iter(self._towers.values()))
        while tower.parent:
            tower = self._towers[tower.parent]
        return tower.name




def _compile_data(line: str) -> _Tower:
    return _Tower.create_tower(line)




class Puzzle(BasicPuzzle):
    def _test_puzzle(self) -> None:
        puzzle_test = list(map(
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
        ]))
        t = _Towers(puzzle_test)
        self._print_test(Fd('tknk', t.find_first_parent, ()))

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file(_compile_data)
        t = _Towers(puzzle_input)
        self._print_result(Fd('hlqnsbe', t.find_first_parent, ()))

    def __init__(self) -> None:
        super().__init__(2017, 7)
