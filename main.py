"""
main module
"""
# for notepad++: find=(?<=.{100})\s, replace=$0\r\n to wrap long lines


import importlib


def solve_puzzle(year: int, day: int) -> None:
    """
    imports the module for the appropriate year and day and solves it
    :param year: year of the puzzle
    :type year: int
    :param day: day of the puzzle
    :type day: int
    :return: None
    :rtype: None
    """
    try:
        puzzle = importlib.import_module(f'puzzles.{year:04d}.day{day:02d}', package=None).Puzzle()
    except ModuleNotFoundError:
        print(f"The puzzle (year: {year}, day: {day}) has not been solved")
    else:
        puzzle.solve()


if __name__ == '__main__':
    solve_puzzle(2024, 11)
