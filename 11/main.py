from itertools import combinations
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
    grid = []

    for input_line in input_lines:
        input_row = [*input_line]
        grid.append(input_row)

    expanded = expand(grid)

    # for row in expanded:
    #     print("".join(row))

    galaxy_locations = []

    for row_index, row in enumerate(expanded):
        for col_index, value in enumerate(row):
            if value == "#":
                galaxy_locations.append((row_index, col_index))

    galaxy_pairs = list(combinations(galaxy_locations, 2))

    distances = []
    for pair in galaxy_pairs:
        a = pair[0]
        b = pair[1]
        distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
        distances.append(distance)

    return str(sum(distances))


def expand(grid, factor=2):
    result = []

    # copy all rows to result
    for row in grid:
        result.append(row)

    # expand rows
    rows_inserted = 0
    for row_index, row in enumerate(grid):
        if all(x == "." for x in row):
            for _ in range(factor - 1):
                result.insert(row_index + rows_inserted, row)
                rows_inserted += 1

    # transpose to do easier column expansion
    transposed_grid = [list(a) for a in zip(*result)]
    result = [list(a) for a in zip(*result)]

    # expand columns
    cols_inserted = 0
    for col_index, column in enumerate(transposed_grid):
        if all(x == "." for x in column):
            for _ in range(factor - 1):
                result.insert(col_index + cols_inserted, column)
                cols_inserted += 1

    return [list(a) for a in zip(*result)]


def solve_part_2(input_lines: list[str]) -> str:
    grid = []

    for input_line in input_lines:
        input_row = [*input_line]
        grid.append(input_row)

    expansion_factor = 1000000
    rows_to_expand = []
    cols_to_expand = []

    for row_index, row in enumerate(grid):
        if all(x == "." for x in row):
            rows_to_expand.append(row_index)

    for col_index, col in enumerate(transpose(grid)):
        if all(x == "." for x in col):
            cols_to_expand.append(col_index)

    galaxy_locations = []
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value == "#":
                galaxy_locations.append((row_index, col_index))

    galaxy_pairs = list(combinations(galaxy_locations, 2))

    distances = []
    for pair in galaxy_pairs:
        a = pair[0]
        b = pair[1]
        distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
        distances.append(distance)

    for expansion_row in rows_to_expand:
        for idx, pair in enumerate(galaxy_pairs):
            a = pair[0]
            b = pair[1]

            if a[0] < expansion_row < b[0] or b[0] < expansion_row < a[0]:
                distances[idx] += expansion_factor - 1

    for expansion_col in cols_to_expand:
        for idx, pair in enumerate(galaxy_pairs):
            a = pair[0]
            b = pair[1]

            if a[1] < expansion_col < b[1] or b[1] < expansion_col < a[1]:
                distances[idx] += expansion_factor - 1

    return str(sum(distances))


def transpose(grid):
    return [list(a) for a in zip(*grid)]


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

    # test_part_2_suite = unittest.TestSuite()
    # test_part_2_suite.addTest(TestSolve("test_sample_part_2"))
    # test_part_2_result = unittest.TextTestRunner().run(test_part_2_suite)

    # if test_part_2_result.wasSuccessful():
    print("Part 2 result:")
    with open("input/input.txt") as input_file:
        input_lines = input_file.read().splitlines()
        print(solve_part_2(input_lines))
