from functools import cache
import unittest

# HEAVILY helped by https://www.reddit.com/r/adventofcode/comments/18hbbxe/2023_day_12python_stepbystep_tutorial_with_bonus/
# could not wrap my head around this recursion for so long


class TestSolve(unittest.TestCase):
    def test_sample_part_1(self):
        with open("input/sample-part-1.txt") as sample_input, open(
            "output/sample-part-1.txt"
        ) as sample_output:
            input_lines = sample_input.read().splitlines()
            output = sample_output.read().strip()
            self.assertEqual(solve_part_1(input_lines), output)

    def test_sample_part_2(self):
        with open("input/sample-part-2.txt") as sample_input, open(
            "output/sample-part-2.txt"
        ) as sample_output:
            input_lines = sample_input.read().splitlines()
            output = sample_output.read().strip()
            self.assertEqual(solve_part_2(input_lines), output)


OPERATIONAL = "."
DAMAGED = "#"
UNKNOWN = "?"


def solve_part_1(input_lines: list[str]) -> str:
    arrangements = 0
    for index, input_line in enumerate(input_lines):
        springs, check = input_line.split()
        check = tuple(int(i) for i in check.split(","))

        arrangements += solve(springs, check)

    return str(arrangements)


def solve_part_2(input_lines: list[str]) -> str:
    possibilities = 0
    for index, input_line in enumerate(input_lines):
        springs, groups = input_line.split()
        springs = UNKNOWN.join([springs] * 5)
        groups = ",".join([groups] * 5)
        groups = tuple(int(i) for i in groups.split(","))
        possibilities += solve(springs, groups)

    return str(possibilities)


@cache
def solve(springs: str, groups: tuple[int]) -> int:
    """Recursively find the total number of valid spring arrangements for the given groups"""
    # base cases
    # ----------
    #
    # no springs, empty group
    # -----------------------
    # solve("", ()) -> 1
    #
    # no springs
    # -----------------------
    # solve("", (1)) -> 0
    #
    # empty group
    # -----------
    # solve("#", ()) -> 0
    # solve(".", ()) -> 1
    #
    # single spring
    # -------------
    # solve("#", (1)) -> 1
    # solve("#", (2)) -> 0
    # solve(".", (1)) -> 0
    # solve(".", (2)) -> 0
    if not groups:
        if DAMAGED not in springs:
            return 1
        else:
            return 0

    if not springs:
        return 0

    # Look at the next element in each record and group
    next_spring = springs[0]
    next_group = groups[0]

    if next_spring == DAMAGED:
        out = handle_damaged(springs, next_group, groups)

    if next_spring == OPERATIONAL:
        out = solve(springs[1:], groups)

    if next_spring == UNKNOWN:
        out = handle_damaged(springs, next_group, groups) + solve(springs[1:], groups)

    # print(springs, groups, out)
    return out


def handle_damaged(springs: str, next_group_size: int, groups: tuple[int]) -> int:
    # next N character must be able to be DAMAGED to match group
    this_group = springs[:next_group_size]
    this_group = this_group.replace("?", "#")

    if this_group != next_group_size * DAMAGED:
        return 0

    if len(springs) == next_group_size:
        if len(groups) == 1:
            return 1
        else:
            return 0

    if springs[next_group_size] in [OPERATIONAL, UNKNOWN]:
        return solve(springs[next_group_size + 1 :], groups[1:])

    return 0


if __name__ == "__main__":
    test_part_1_suite = unittest.TestSuite()
    test_part_1_suite.addTest(TestSolve("test_sample_part_1"))
    test_part_1_result = unittest.TextTestRunner().run(test_part_1_suite)

    if test_part_1_result.wasSuccessful():
        print("Part 1 result:")
        with open("input/input.txt") as input_file:
            input_lines = input_file.read().splitlines()
            print(solve_part_1(input_lines))
    else:
        exit()

    test_part_2_suite = unittest.TestSuite()
    test_part_2_suite.addTest(TestSolve("test_sample_part_2"))
    test_part_2_result = unittest.TextTestRunner().run(test_part_2_suite)

    if test_part_2_result.wasSuccessful():
        print("Part 2 result:")
        with open("input/input.txt") as input_file:
            input_lines = input_file.read().splitlines()
            print(solve_part_2(input_lines))
