from enum import Enum
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


class Tile(Enum):
    NORTH_SOUTH = "|"
    EAST_WEST = "-"
    NORTH_EAST = "L"
    NORTH_WEST = "J"
    SOUTH_WEST = "7"
    SOUTH_EAST = "F"
    GROUND = "."
    START = "S"


def solve_part_1(input_lines: list[str]) -> str:
    grid = []

    # construct grid with padding
    grid.append([Tile.GROUND.value] * (len(input_lines[0]) + 2))

    for input_line in input_lines:
        grid.append([Tile.GROUND.value, *input_line, Tile.GROUND.value])

    grid.append([Tile.GROUND.value] * (len(input_lines[0]) + 2))

    # (row, col)
    start_index = (-1, -1)
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value == Tile.START.value:
                start_index = (row_index, col_index)

    # print(f"Start index: {start_index[0], start_index[1]}")
    visited = set()
    next_index = (-1, -1)
    loop_length = 0
    connected_pipes = get_connected_pipes(start_index, grid)

    # pick first one to traverse
    next_index = connected_pipes[0]
    visited.add(next_index)
    loop_length += 1

    while next_index != start_index:
        # print(f"At {grid[next_index[0]][next_index[1]]}")
        connected_pipes = get_connected_pipes(next_index, grid)
        # print(connected_pipes)

        if connected_pipes[0] in visited:
            next_index = connected_pipes[1]
        else:
            next_index = connected_pipes[0]

        loop_length += 1
        visited.add(next_index)

    return str(loop_length // 2)


def get_connected_pipes(index: tuple, grid: list[list]):
    row, col = index

    connected_pipe_indices = []
    pipe = grid[index[0]][index[1]]

    north = grid[row - 1][col]
    east = grid[row][col + 1]
    south = grid[row + 1][col]
    west = grid[row][col - 1]

    if (
        pipe == Tile.START.value
        or pipe == Tile.NORTH_SOUTH.value
        or pipe == Tile.NORTH_EAST.value
        or pipe == Tile.NORTH_WEST.value
    ) and (
        north == Tile.NORTH_SOUTH.value
        or north == Tile.SOUTH_EAST.value
        or north == Tile.SOUTH_WEST.value
        or north == Tile.START.value
    ):
        connected_pipe_indices.append((row - 1, col))

    if (
        pipe == Tile.START.value
        or pipe == Tile.EAST_WEST.value
        or pipe == Tile.NORTH_EAST.value
        or pipe == Tile.SOUTH_EAST.value
    ) and (
        east == Tile.EAST_WEST.value
        or east == Tile.NORTH_WEST.value
        or east == Tile.SOUTH_WEST.value
        or east == Tile.START.value
    ):
        connected_pipe_indices.append((row, col + 1))

    if (
        pipe == Tile.START.value
        or pipe == Tile.NORTH_SOUTH.value
        or pipe == Tile.SOUTH_EAST.value
        or pipe == Tile.SOUTH_WEST.value
    ) and (
        south == Tile.NORTH_SOUTH.value
        or south == Tile.NORTH_EAST.value
        or south == Tile.NORTH_WEST.value
        or south == Tile.START.value
    ):
        connected_pipe_indices.append((row + 1, col))

    if (
        pipe == Tile.START.value
        or pipe == Tile.EAST_WEST.value
        or pipe == Tile.NORTH_WEST.value
        or pipe == Tile.SOUTH_WEST.value
    ) and (
        west == Tile.EAST_WEST.value
        or west == Tile.NORTH_EAST.value
        or west == Tile.SOUTH_EAST.value
        or west == Tile.START.value
    ):
        connected_pipe_indices.append((row, col - 1))

    return connected_pipe_indices


def solve_part_2(input_lines: list[str]) -> str:
    # TODO: count by rows, all tiles with ODD vertical crossing as inside, EVEN as outside
    grid = []

    # construct grid with padding
    grid.append([Tile.GROUND.value] * (len(input_lines[0]) + 2))

    for input_line in input_lines:
        grid.append([Tile.GROUND.value, *input_line, Tile.GROUND.value])

    grid.append([Tile.GROUND.value] * (len(input_lines[0]) + 2))

    # (row, col)
    start_index = (-1, -1)
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value == Tile.START.value:
                start_index = (row_index, col_index)

    grid[start_index[0]][start_index[1]] = compute_start_pipe(start_index, grid)

    loop_indices = set()

    connected_pipes = get_connected_pipes(start_index, grid)
    next_index = connected_pipes[0]
    end_index = connected_pipes[1]

    loop_indices.add(start_index)
    loop_indices.add(next_index)

    while next_index != end_index:
        connected_pipes = get_connected_pipes(next_index, grid)

        if connected_pipes[0] in loop_indices:
            next_index = connected_pipes[1]
        else:
            next_index = connected_pipes[0]

        loop_indices.add(next_index)

    loop_indices.add(end_index)

    enclosed_tile_count = 0
    enclosed_tiles = []
    for row_index, row in enumerate(grid):
        vertical_changes = 0

        for col_index, value in enumerate(row):
            if (row_index, col_index) not in loop_indices:
                if vertical_changes % 2 == 1:
                    enclosed_tile_count += 1
                    enclosed_tiles.append((row_index, col_index))
            else:
                if value == Tile.NORTH_SOUTH.value:
                    vertical_changes += 1
                    continue

                # if going up and last non-horizontal was going down
                #   vertical_changes += 1
                if value == Tile.NORTH_WEST.value:
                    for i in range(col_index):
                        prev_tile = row[col_index - i - 1]

                        if (
                            prev_tile == Tile.SOUTH_EAST.value
                            and (row_index, col_index - i - 1) in loop_indices
                        ):
                            vertical_changes += 1
                            break
                        elif (
                            prev_tile == Tile.EAST_WEST.value
                            and (row_index, col_index - i - 1) in loop_indices
                        ):
                            continue
                        else:
                            break

                # if going down and last non-horizontal was going up
                #   vertical_changes += 1
                if value == Tile.SOUTH_WEST.value:
                    for i in range(col_index):
                        prev_tile = row[col_index - i - 1]

                        if (
                            prev_tile == Tile.NORTH_EAST.value
                            and (row_index, col_index - i - 1) in loop_indices
                        ):
                            vertical_changes += 1
                            break
                        elif (
                            prev_tile == Tile.EAST_WEST.value
                            and (row_index, col_index - i - 1) in loop_indices
                        ):
                            continue
                        else:
                            break

    return str(enclosed_tile_count)


def compute_start_pipe(start_index, grid):
    row, col = start_index

    north = (row - 1, col)
    east = (row, col + 1)
    south = (row + 1, col)
    west = (row, col - 1)

    connected_pipes = get_connected_pipes(start_index, grid)
    first = connected_pipes[0]
    second = connected_pipes[1]

    if first == north or second == north:
        if second == east or first == east:
            return Tile.NORTH_EAST.value
        if second == south or first == south:
            return Tile.NORTH_SOUTH.value
        if second == west or first == west:
            return Tile.NORTH_WEST.value

    if first == east or second == east:
        if second == north or first == north:
            return Tile.NORTH_EAST.value
        if second == south or first == south:
            return Tile.SOUTH_EAST.value
        if second == west or first == west:
            return Tile.EAST_WEST.value

    if first == south or second == south:
        if second == north or first == north:
            return Tile.NORTH_SOUTH.value
        if second == east or first == east:
            return Tile.SOUTH_EAST.value
        if second == west or first == west:
            return Tile.SOUTH_WEST.value

    raise ValueError


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
