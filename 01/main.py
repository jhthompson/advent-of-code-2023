import unittest


class TestSolve(unittest.TestCase):
    def test_sample_part_1(self):
        with open("input/sample-part-1.txt") as sample_input, open(
            "output/sample-part-1.txt"
        ) as sample_output:
            input_lines = sample_input.readlines()
            output_lines = sample_output.readlines()
            self.assertEqual(solve_part_1(input_lines), output_lines)

    def test_sample_part_2(self):
        with open("input/sample-part-2.txt") as sample_input, open(
            "output/sample-part-2.txt"
        ) as sample_output:
            input_lines = sample_input.readlines()
            output_lines = sample_output.readlines()
            self.assertEqual(solve_part_2(input_lines), output_lines)


def solve_part_1(input_lines: list[str]) -> list[str]:
    total_calibration_value = 0

    for line in input_lines:
        digits = [i for i in line if i.isdigit()]
        line_calibration_value = int(digits[0] + digits[-1])
        total_calibration_value += line_calibration_value

    return [str(total_calibration_value)]


VALID_STRING_DIGITS = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def solve_part_2(input_lines: list[str]) -> list[str]:
    total_calibration_value = 0

    for line in input_lines:
        lowest_index: int = len(line) - 1
        highest_index: int = 0

        lowest_digit = 0
        highest_digit = 0

        for digit in VALID_STRING_DIGITS:
            lowest_digit_index: int = line.find(digit)
            highest_digit_index: int = line.rfind(digit)

            if highest_digit_index != -1 and highest_digit_index >= highest_index:
                highest_index = highest_digit_index
                highest_digit = VALID_STRING_DIGITS[digit]

            if lowest_digit_index != -1 and lowest_digit_index <= lowest_index:
                lowest_index = lowest_digit_index
                lowest_digit = VALID_STRING_DIGITS[digit]

        total_calibration_value += int(str(lowest_digit) + str(highest_digit))

    return [str(total_calibration_value)]


def check_valid_digit(string: str) -> bool:
    return False


if __name__ == "__main__":
    test_part_1_suite = unittest.TestSuite()
    test_part_1_suite.addTest(TestSolve("test_sample_part_1"))
    test_part_1_result = unittest.TextTestRunner().run(test_part_1_suite)

    if test_part_1_result.wasSuccessful():
        print("Part 1 result:")
        with open("input/input.txt") as input_file:
            input_lines = input_file.readlines()
            print(solve_part_1(input_lines))
    else:
        exit()

    test_part_2_suite = unittest.TestSuite()
    test_part_2_suite.addTest(TestSolve("test_sample_part_2"))
    test_part_2_result = unittest.TextTestRunner().run(test_part_2_suite)

    if test_part_2_result.wasSuccessful():
        print("Part 2 result:")
        with open("input/input.txt") as input_file:
            input_lines = input_file.readlines()
            print(solve_part_2(input_lines))
