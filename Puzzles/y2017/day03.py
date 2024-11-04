"""
"""

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd



def _compile_data(line: str) -> int:
    return int(line)



# TODO: find more mathematical approach
def _get_radii(field: int) -> tuple:
    radius = 0
    max_outer_field = 1
    edge_length = 1
    result = [(radius, max_outer_field, max_outer_field, 1)]
    while True:
        if max_outer_field >= field:
            break
        min_outer_field = max_outer_field + 1
        edge_length += 2
        max_outer_field += edge_length * 4 - 4
        radius += 1
        result.append((radius, min_outer_field, max_outer_field, edge_length))
    return tuple(result)



def _get_pos(field: int) -> tuple[int, int]:
    radii = _get_radii(field)
    radius = -1
    for i in radii:
        if i[1] <= field <= i[2]:
            radius = i
    result = [radius[0], -radius[0]]
    max_distance = radius[3] // 2
    decrease = True
    for i in range(radius[1], field + 1):
        if decrease:
            result[1] -= 1
            if result[1] <= 0:
                distance = 0
                decrease = False
        else:
            result[1] += 1
            if result[1] >= max_distance:
                decrease = True



class _Spiral:
    _RIGHT = 'right'
    _LEFT = 'left'
    _UP = 'top'
    _DOWN = 'down'

    def __init__(self, fields: object) -> None:
        self._fields = fields
        self.position = [0, 0]

    @classmethod
    def _get_direction(cls) -> str:
        while True:
            yield cls._RIGHT
            yield cls._UP
            yield cls._LEFT
            yield cls._DOWN

    def _create_spiral(self) -> None:
        direction_generator = self._get_direction()
        count = 0
        while count <= self._fields:
            direction = next(direction_generator)

    def _next_pos(self, direction: str):
        match direction:
            case self._RIGHT:
                self.position[0] += 1
            case self._LEFT:
                self.position[0] -= 1
            case self._UP:
                self.position[1] -= 1
            case self._DOWN:
                self.position[1] += 1



def _get_distance(field: int) -> int:
    radii = _get_radii(field)
    radius = -1
    for i in radii:
        if i[1] <= field <= i[2]:
            radius = i
    distance = radius[0]
    max_distance = radius[3] // 2
    decrease = True
    for i in range(radius[1], field + 1):
        if decrease:
            distance -= 1
            if distance <= 0:
                distance = 0
                decrease = False
        else:
            distance += 1
            if distance >= max_distance:
                decrease = True
    return radius[0] + distance



class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2017, 3)
        puzzle_input = self._read_file(_compile_data)[0]

        # self._add_tests(
        #     [
        #         Fd(0, _get_distance, (1,)),
        #         Fd(3, _get_distance, (12,)),
        #         Fd(2, _get_distance, (23,)),
        #         Fd(31, _get_distance, (1024,)),
        #     ]
        # )
        #
        # self._add_result(Fd(480, _get_distance, (puzzle_input,)))
        # self._add_result(Fd(1152, _sum_digits_part2, (puzzle_input,)))
