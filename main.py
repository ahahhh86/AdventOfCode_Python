"""
main module
"""
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
    solve_puzzle(2024, 7)
# import multiprocessing
#
#
# def worker(numbers, start, end, result):
#     """A worker function to calculate squares of numbers."""
#     for i in range(start, end):
#         result[i] = numbers[i] * numbers[i]
#
# def main(core_count):
#     numbers = range(10000)  # A larger range for a more evident effect of multiprocessing
#     result = multiprocessing.Array('i', len(numbers))
#     segment = len(numbers) // core_count
#     processes = []
#
#     for i in range(core_count):
#         start = i * segment
#         if i == core_count - 1:
#             end = len(numbers)  # Ensure the last segment goes up to the end
#         else:
#             end = start + segment
#         # Creating a process for each segment
#         p = multiprocessing.Process(target=worker, args=(numbers, start, end, result))
#         processes.append(p)
#         p.start()
#
#     for p in processes:
#         p.join()
#
#     return result
#
# if __name__ == '__main__':
#     for core_count in [2, 4, 8]:
#         print(f"Using {core_count} cores:")
#         result = main(core_count)
#         print(f"First 10 squares: {list(result)[:10]}")  # Display the first 10 results as a sample
