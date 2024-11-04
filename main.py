import importlib

def solve_puzzle(year: int, day: int) -> None:
    puzzle = importlib.import_module(f'Puzzles.y{year:04d}.day{day:02d}', package=None).Puzzle()
    puzzle.solve()


if __name__ == '__main__':
    # solve_puzzle(2017, 1)
    # solve_puzzle(2017, 2)
    solve_puzzle(2017, 3)
