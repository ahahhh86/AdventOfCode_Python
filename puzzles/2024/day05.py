"""
"""

from black.trans import defaultdict

from tools.basic_puzzle import BasicPuzzle, FunctionData as Fd


class _Updates:
    def __init__(self, data: str) -> None:
        self._incorrect_middle_sum = 0
        order_list, update_list = data.split("\n\n")

        self._order = defaultdict(list)
        for line in order_list.splitlines():
            x, y = line.split("|")
            self._order[int(x)].append(int(y))

        self._updates = []
        for line in update_list.splitlines():
            self._updates.append([int(i) for i in line.split(",")])

    def sum_correct_middle(self):
        result = 0
        for update in self._updates:
            if self._has_right_order(update):
                result += update[len(update) // 2]
            else:
                self._sort(update)
                self._incorrect_middle_sum += update[len(update) // 2]
        return result

    def sum_incorrect_middle(self):
        return self._incorrect_middle_sum

    def _has_right_order(self, updates: list[int]) -> bool:
        for index, update in enumerate(updates):
            for after in self._order[update]:
                if after in updates[:index]:
                    return False
        return True

    def _sort(self, updates: list[int]):
        pass


class Puzzle(BasicPuzzle):
    def __init__(self) -> None:
        super().__init__(2024, 5)

    def _test_puzzle(self) -> None:
        updates = _Updates(
            """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
        )
        self._print_test(Fd(143, updates.sum_correct_middle, ()))
        self._print_test(Fd(123, updates.sum_incorrect_middle, ()))

    def _solve_puzzle(self) -> None:
        updates = _Updates(self.read_file())
        self._print_result(Fd(5713, updates.sum_correct_middle, ()))
        self._print_result(Fd(0, updates.sum_incorrect_middle, ()))
