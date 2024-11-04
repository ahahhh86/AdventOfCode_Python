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
    abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first
word.
    a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another
word.
    iiii oiii ooii oooi oooo is valid.
    oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.

Under this new system policy, how many passphrases are valid?

Your puzzle answer was 265.
"""

from collections import Counter
from functools import reduce

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd



def _compile_data(line: str) -> tuple[str, ...]:
    return tuple(line.split())



def _count_valid(phrases: tuple, function: callable) -> int:
    return sum(1 for phrase in phrases if function(phrase))


def _count_valid_passphrases_part1(phrases: tuple[str, ...]) -> int:
    return _count_valid(phrases, lambda phrase: len(phrase) == len(set(phrase)))



def _count_valid_passphrases_part2(phrases: tuple[str, ...]) -> int:
    def _is_valid(phrase: str) -> int:
        letters_of_words = [Counter(word) for word in phrase]
        while letters_of_words:
            letters = letters_of_words.pop()
            if letters in letters_of_words:
                return False
        return True

    return _count_valid(phrases, _is_valid)



class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2017, 4)
        puzzle_input = self._read_file(_compile_data)

        self._add_tests(
            [
                Fd(1, _count_valid_passphrases_part1, ([('aa,' 'bb', 'cc', 'dd', 'ee',)],)),
                Fd(0, _count_valid_passphrases_part1, ([('aa', 'bb', 'cc', 'dd', 'aa',)],)),
                Fd(1, _count_valid_passphrases_part1, ([('aa', 'bb', 'cc', 'dd', 'aaa',)],)),
                None,
                Fd(1, _count_valid_passphrases_part2, ([('abcde', 'fghij',)],)),
                Fd(0, _count_valid_passphrases_part2, ([('abcde', 'xyz', 'ecdab',)],)),
                Fd(1, _count_valid_passphrases_part2, ([('a', 'ab', 'abc', 'abd', 'abf', 'abj',)],)),
                Fd(1, _count_valid_passphrases_part2, ([('iiii', 'oiii', 'ooii', 'oooi', 'oooo',)],)),
                Fd(0, _count_valid_passphrases_part2, ([('oiii', 'ioii', 'iioi', 'iiio',)],)),
            ]
        )

        self._add_result(Fd(383, _count_valid_passphrases_part1, (puzzle_input,)))
        self._add_result(Fd(265, _count_valid_passphrases_part2, (puzzle_input,)))