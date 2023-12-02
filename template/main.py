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
    # TODO: fill out
    return ""


def solve_part_2(input_lines: list[str]) -> str:
    # TODO: fill out
    return ""


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
