import importlib

# todo: make dynamic
import Puzzles.y2017.day01
import Puzzles.y2017.day02



def solve2017(day: int) -> None:
    class_name = f'Puzzles.y2017.day{day:02d}.Puzzle()'
    puzzle = eval(class_name)
    puzzle.solve()
