"""
--- Day 4: High-Entropy Passphrases ---

A new system policy has been put in place that requires all accounts to use a passphrase instead of simply
a password. A passphrase consists of a series of words (lowercase letters) separated by spaces.

To ensure security, a valid passphrase must contain no duplicate words.

For example:
    aa bb cc dd ee is valid.
    aa bb cc dd aa is not valid - the word aa appears more than once.
    aa bb cc dd aaa is valid - aa and aaa count as different words.

The system's full passphrase list is available as your puzzle input. How many passphrases are valid?


Your puzzle answer was 383.

--- Part Two ---
For added security, yet another system policy has been put in place. Now, a valid passphrase must contain
no two words that are anagrams of each other - that is, a passphrase is invalid if any word's letters
can be rearranged to form any other word in the passphrase.

For example:
    abcde fghij is a valid passphrase.
    abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first word.
    a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another word.
    iiii oiii ooii oooi oooo is valid.
    oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.

Under this new system policy, how many passphrases are valid?

Your puzzle answer was 265.
"""

from collections import Counter

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd
from tools.generic_functions import count_if


def _count_valid_passphrases_part1(phrases: tuple[str, ...]) -> int:
    return count_if(lambda phrase: len(phrase) == len(set(phrase)), phrases)


def _count_valid_passphrases_part2(phrases: tuple[str, ...]) -> int:
    def _is_valid(phrase: str) -> int:
        letters_of_words = [Counter(word) for word in phrase]
        while letters_of_words:
            letters = letters_of_words.pop()
            if letters in letters_of_words:
                return False
        return True

    return count_if(_is_valid, phrases)


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2017, 4)

    def _test_puzzle(self) -> None:
        self._print_test(Fd(1, _count_valid_passphrases_part1, ([('aa,' 'bb', 'cc', 'dd', 'ee',)],)))
        self._print_test(Fd(0, _count_valid_passphrases_part1, ([('aa', 'bb', 'cc', 'dd', 'aa',)],)))
        self._print_test(Fd(1, _count_valid_passphrases_part1, ([('aa', 'bb', 'cc', 'dd', 'aaa',)],)))
        print()
        self._print_test(Fd(1, _count_valid_passphrases_part2, ([('abcde', 'fghij',)],)))
        self._print_test(Fd(0, _count_valid_passphrases_part2, ([('abcde', 'xyz', 'ecdab',)],)))
        self._print_test(Fd(1, _count_valid_passphrases_part2, ([('a', 'ab', 'abc', 'abd', 'abf', 'abj',)],)))
        self._print_test(Fd(1, _count_valid_passphrases_part2, ([('iiii', 'oiii', 'ooii', 'oooi', 'oooo',)],)))
        self._print_test(Fd(0, _count_valid_passphrases_part2, ([('oiii', 'ioii', 'iioi', 'iiio',)],)))

    def _solve_puzzle(self) -> None:
        puzzle_input = self.read_file(lambda line: tuple(line.split()))
        self._print_result(Fd(383, _count_valid_passphrases_part1, (puzzle_input,)))
        self._print_result(Fd(265, _count_valid_passphrases_part2, (puzzle_input,)))
