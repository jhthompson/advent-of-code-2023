from itertools import pairwise
import unittest


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


def solve_part_1(input_lines: list[str]) -> str:
    # 0   3   6   9  12  15  _18_
    #   3   3   3   3   3  _3_
    #     0   0   0   0  _0_

    # 10  13  16  21  30  45  _68_
    #   3   3   5   9   15  _23_
    #     0   2   4   6   _8_
    #       2   2   2   _2_
    #         0   0   _0_

    next_values = []
    for input_line in input_lines:
        sequences = []

        history = [int(i) for i in input_line.split()]
        sequences.append(history)

        while True:
            sequence = sequences[-1]
            next_sequence = []

            for left, right in pairwise(sequence):
                diff = right - left
                next_sequence.append(diff)

            sequences.append(next_sequence)

            if all([x == 0 for x in next_sequence]):
                break

        increment = 0
        for s in reversed(sequences):
            increment += s[-1]

        next_values.append(increment)

    return str(sum(next_values))


def solve_part_2(input_lines: list[str]) -> str:
    # _5_  10  13  16  21  30  45
    #   _5_   3   3   5   9  15
    #    _-2_   0   2   4   6
    #       _2_   2   2   2
    #         _0_   0   0

    previous_values = []
    for input_line in input_lines:
        sequences = []

        history = [int(i) for i in input_line.split()]
        sequences.append(history)

        while True:
            sequence = sequences[-1]
            next_sequence = []

            for left, right in pairwise(sequence):
                diff = right - left
                next_sequence.append(diff)

            sequences.append(next_sequence)

            if all([x == 0 for x in next_sequence]):
                break

        previous = 0
        for s in reversed(sequences):
            previous = s[0] - previous

        previous_values.append(previous)

    return str(sum(previous_values))


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
