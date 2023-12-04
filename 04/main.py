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
    point_total = 0
    for line in input_lines:
        card_string, numbers_string = line.split(":")
        winning_numbers_string, my_numbers = numbers_string.split("|")
        winning_numbers = set(winning_numbers_string.strip().split())
        my_numbers = set(my_numbers.strip().split())
        common_numbers = len(winning_numbers.intersection(my_numbers))

        # 1 winning number (2 ^ 0) -> 1 point
        # 2 (2 ^ 1) -> 2
        # 3 (2 ^ 2) -> 4
        # 4 (2 ^ 3) -> 8
        # 5 (2 ^ 4) -> 16
        # 6 (2 ^ 5) -> 32
        if common_numbers:
            point_total += 2 ** (common_numbers - 1)

    return str(point_total)


def solve_part_2(input_lines: list[str]) -> str:
    card_count = [1] * len(input_lines)

    for index, line in enumerate(input_lines):
        card_string, numbers_string = line.split(":")
        winning_numbers_string, my_numbers = numbers_string.split("|")
        winning_numbers = set(winning_numbers_string.strip().split())
        my_numbers = set(my_numbers.strip().split())
        common_numbers = len(winning_numbers.intersection(my_numbers))

        for i in range(common_numbers):
            for _ in range(card_count[index]):
                card_count[index + 1 + i] += 1

    return str(sum(card_count))


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
