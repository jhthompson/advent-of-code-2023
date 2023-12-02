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
    valid_ids = []
    for line in input_lines:
        game_id = parse_game_id(line)
        rounds = parse_rounds(line)

        if possible(rounds):
            valid_ids.append(game_id)

    return str(sum(valid_ids))


def possible(rounds: list[dict[str, int]]) -> bool:
    REDS = 12
    GREENS = 13
    BLUES = 14

    for round in rounds:
        if round["red"] > REDS:
            return False

        if round["green"] > GREENS:
            return False

        if round["blue"] > BLUES:
            return False

    return True


def parse_game_id(line: str) -> int:
    return int(line.split(":")[0].replace("Game ", ""))


def parse_rounds(line: str) -> list[dict[str, int]]:
    all_rounds_string: str = line.split(": ")[1]
    rounds_strings = all_rounds_string.split("; ")

    rounds = []

    for rounds_string in rounds_strings:
        round = {"red": 0, "green": 0, "blue": 0}

        for dice_string in rounds_string.split(", "):
            amount, color = dice_string.split(" ")
            round[color] = int(amount)

        rounds.append(round)

    return rounds


def solve_part_2(input_lines: list[str]) -> str:
    sum_of_powers = 0
    for line in input_lines:
        rounds = parse_rounds(line)

        min_red = 0
        min_green = 0
        min_blue = 0

        for round in rounds:
            if round["red"] > min_red:
                min_red = round["red"]

            if round["green"] > min_green:
                min_green = round["green"]

            if round["blue"] > min_blue:
                min_blue = round["blue"]

        sum_of_powers += min_red * min_green * min_blue

    return str(sum_of_powers)


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
