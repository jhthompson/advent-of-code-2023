from math import lcm
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
    instructions = input_lines[0]
    node_lines = input_lines[2:]
    nodes = {}

    for node_line in node_lines:
        start, destinations = node_line.split(" = ")
        left = destinations[1:4]
        right = destinations[6:9]

        nodes[start] = (left, right)

    curr_node = "AAA"
    steps = 0

    while curr_node != "ZZZ":
        instruction = instructions[steps % len(instructions)]

        steps += 1
        node = nodes[curr_node]

        if instruction == "L":
            curr_node = node[0]
        elif instruction == "R":
            curr_node = node[1]
        else:
            raise ValueError

        if curr_node == "ZZZ":
            break

    return str(steps)


def solve_part_2(input_lines: list[str]) -> str:
    instructions = input_lines[0]
    node_lines = input_lines[2:]
    nodes: dict[str, tuple] = {}

    for node_line in node_lines:
        start, destinations = node_line.split(" = ")
        left = destinations[1:4]
        right = destinations[6:9]

        nodes[start] = (left, right)

    starting_nodes = [n for n in nodes.keys() if n.endswith("A")]
    steps_to_finish = []

    for starting_node in starting_nodes:
        curr_node = starting_node
        steps = 0

        while not curr_node.endswith("Z"):
            instruction = instructions[steps % len(instructions)]

            steps += 1
            node = nodes[curr_node]

            if instruction == "L":
                curr_node = node[0]
            elif instruction == "R":
                curr_node = node[1]
            else:
                raise ValueError

        steps_to_finish.append(steps)

    return str(lcm(*steps_to_finish))


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
