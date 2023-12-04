from collections import defaultdict
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
    grid: list[list[str]] = []
    part_numbers = []
    other_numbers = []
    invalid_positions = set()

    numbers_by_start_position: dict[tuple, int] = {}
    symbol_positions: set[tuple] = set()

    for line in input_lines:
        grid.append(list(line))

    for row_index, row in enumerate(grid):
        curr_number_start_position = (-1, -1)
        curr_number = ""

        for col_index, col in enumerate(row):
            if col in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                if not curr_number:
                    curr_number_start_position = (row_index, col_index)
                curr_number += col

                # if current number ends on the end of a line
                if col_index == len(row) - 1 and curr_number:
                    numbers_by_start_position[curr_number_start_position] = int(
                        curr_number
                    )
            else:
                if curr_number:
                    numbers_by_start_position[curr_number_start_position] = int(
                        curr_number
                    )
                curr_number = ""
                curr_number_start_position = (-1, -1)

                if col != ".":
                    symbol_positions.add((row_index, col_index))

    # for each number, check for any symbols around it
    for number_start_position, number in numbers_by_start_position.items():
        if number_adjacent_to_symbol(number_start_position, number, symbol_positions):
            part_numbers.append(number)
        else:
            invalid_positions.add(number_start_position)
            row_start, col_start = number_start_position

            for i in range(len(str(number)) - 1):
                invalid_positions.add((row_start, col_start + i + 1))

            other_numbers.append(number)

    # for row_index, row in enumerate(grid):
    #     for col_index, col in enumerate(row):
    #         if (row_index, col_index) in invalid_positions:
    #             print(f"\033[0;31m{col}\033[0m", end="")
    #         elif (row_index, col_index) in symbol_positions:
    #             print(f"\033[1;32;40m{col}\033[0m", end="")
    #         else:
    #             print(col, end="")

    #     print()

    # print(part_numbers)

    return str(sum(part_numbers))


def number_adjacent_to_symbol(
    number_start_position: tuple, number: int, symbol_positions: set[tuple]
):
    number_positions = [number_start_position]
    row_start, col_start = number_start_position

    for i in range(len(str(number)) - 1):
        number_positions.append((row_start, col_start + i + 1))

    for position in number_positions:
        row, col = position

        if (
            (row - 1, col) in symbol_positions  # top
            or (row - 1, col + 1) in symbol_positions  # top right
            or (row, col + 1) in symbol_positions  # right
            or (row + 1, col + 1) in symbol_positions  # bottom right
            or (row + 1, col) in symbol_positions  # bottom
            or (row + 1, col - 1) in symbol_positions  # bottom left
            or (row, col - 1) in symbol_positions  # left
            or (row - 1, col - 1) in symbol_positions  # top left
        ):
            return True

    return False


def solve_part_2(input_lines: list[str]) -> str:
    grid: list[list[str]] = []
    part_numbers = []
    other_numbers = []
    invalid_positions = set()

    numbers_by_start_position: dict[tuple, int] = {}
    part_numbers_by_start_position: dict[tuple, int] = {}
    symbol_positions: set[tuple] = set()

    adjacent_numbers_by_gear: dict[tuple, list[int]] = defaultdict(list)

    for line in input_lines:
        grid.append(list(line))

    for row_index, row in enumerate(grid):
        curr_number_start_position = (-1, -1)
        curr_number = ""

        for col_index, col in enumerate(row):
            if col in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                if not curr_number:
                    curr_number_start_position = (row_index, col_index)
                curr_number += col

                # if current number ends on the end of a line
                if col_index == len(row) - 1 and curr_number:
                    numbers_by_start_position[curr_number_start_position] = int(
                        curr_number
                    )
            else:
                if curr_number:
                    numbers_by_start_position[curr_number_start_position] = int(
                        curr_number
                    )
                curr_number = ""
                curr_number_start_position = (-1, -1)

                if col != ".":
                    symbol_positions.add((row_index, col_index))

    # for each number, check for any symbols around it
    for number_start_position, part_number in numbers_by_start_position.items():
        if number_adjacent_to_symbol(
            number_start_position, part_number, symbol_positions
        ):
            part_numbers.append(part_number)
            part_numbers_by_start_position[number_start_position] = part_number
        else:
            invalid_positions.add(number_start_position)
            row_start, col_start = number_start_position

            for i in range(len(str(part_number)) - 1):
                invalid_positions.add((row_start, col_start + i + 1))

            other_numbers.append(part_number)

    # for each part number
    # get any adjacent gears
    # store that somewhere
    # adjacent_numbers_by_gear[gear_position].add(number)
    for (
        part_number_start_position,
        part_number,
    ) in part_numbers_by_start_position.items():
        part_number_positions = [part_number_start_position]
        row_start, col_start = part_number_start_position

        for i in range(len(str(part_number)) - 1):
            part_number_positions.append((row_start, col_start + i + 1))

        for position in part_number_positions:
            row, col = position

            try:
                if grid[row - 1][col] == "*":  # top
                    adjacent_numbers_by_gear[(row - 1, col)].append(part_number)
                    break
                if grid[row - 1][col + 1] == "*":  # top right
                    adjacent_numbers_by_gear[(row - 1, col + 1)].append(part_number)
                    break

                if grid[row][col + 1] == "*":  # right
                    adjacent_numbers_by_gear[(row, col + 1)].append(part_number)
                    break

                if grid[row + 1][col + 1] == "*":  # bottom right
                    adjacent_numbers_by_gear[(row + 1, col + 1)].append(part_number)
                    break

                if grid[row + 1][col] == "*":  # bottom
                    adjacent_numbers_by_gear[(row + 1, col)].append(part_number)
                    break

                if grid[row + 1][col - 1] == "*":  # bottom left
                    adjacent_numbers_by_gear[(row + 1, col - 1)].append(part_number)
                    break

                if grid[row][col - 1] == "*":  # left
                    adjacent_numbers_by_gear[(row, col - 1)].append(part_number)
                    break

                if grid[row - 1][col - 1] == "*":  # top left
                    adjacent_numbers_by_gear[(row - 1, col - 1)].append(part_number)
                    break
            except IndexError:
                pass

    gear_ratios = []
    for (
        gear_position,
        adjacent_part_numbers,
    ) in adjacent_numbers_by_gear.items():
        if (len(adjacent_part_numbers)) == 2:
            gear_ratios.append(adjacent_part_numbers[0] * adjacent_part_numbers[1])

    return str(sum(gear_ratios))

    # for row_index, row in enumerate(grid):
    #     for col_index, col in enumerate(row):
    #         if (row_index, col_index) in invalid_positions:
    #             print(f"\033[0;31m{col}\033[0m", end="")
    #         elif (row_index, col_index) in symbol_positions:
    #             print(f"\033[1;32;40m{col}\033[0m", end="")
    #         else:
    #             print(col, end="")

    #     print()

    # print(part_numbers)

    return str(sum(part_numbers))


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
