from collections import defaultdict
from itertools import islice
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
    seeds_line = input_lines[0]
    seeds = [int(i) for i in seeds_line.split(": ")[1].split()]

    current_map = ("seed", "soil")  # currently looking at "seed-to-soil-map"
    mappings_by_type = defaultdict(
        list
    )  # i.e. { ("seed", "soil"): [ (50, 98, 2), (52, 50, 48)] }
    for line in input_lines[2:]:
        if line.endswith("map:"):
            current_map = tuple(line.split()[0].split("-to-"))
        elif not line:
            continue  # end of current map data
        else:
            # bulk of the processing is here
            destination_range_start, source_range_start, range_length = [
                int(i) for i in line.split()
            ]
            mappings_by_type[current_map].append(
                (destination_range_start, source_range_start, range_length)
            )

    locations = []
    for seed in seeds:
        soil = do_lookup(seed, mappings_by_type[("seed", "soil")])
        fertilizer = do_lookup(soil, mappings_by_type[("soil", "fertilizer")])
        water = do_lookup(fertilizer, mappings_by_type[("fertilizer", "water")])
        light = do_lookup(water, mappings_by_type[("water", "light")])
        temperature = do_lookup(light, mappings_by_type[("light", "temperature")])
        humidity = do_lookup(temperature, mappings_by_type[("temperature", "humidity")])
        location = do_lookup(humidity, mappings_by_type[("humidity", "location")])

        locations.append(location)

    return str(min(locations))


def do_lookup(source_number: int, mappings: list[tuple]):
    for mapping in mappings:
        destination_range_start, source_range_start, range_length = mapping

        if source_number in range(
            source_range_start, source_range_start + range_length
        ):
            offset = source_number - source_range_start

            return destination_range_start + offset

    return source_number


def solve_part_2(input_lines: list[str]) -> str:
    seeds_line = input_lines[0]
    seeds = [int(i) for i in seeds_line.split(": ")[1].split()]
    seed_range_pairs = batched(seeds, 2)

    seed_ranges: list[range] = []  # (start, end)
    for start_seed, count in seed_range_pairs:
        seed_ranges.append((start_seed, start_seed + count))

    current_map = ("seed", "soil")  # currently looking at "seed-to-soil-map"
    mappings_by_type = defaultdict(
        list
    )  # i.e. { ("seed", "soil"): [ (50, 98, 2), (52, 50, 48)] }
    for line in input_lines[2:]:
        if line.endswith("map:"):
            current_map = tuple(line.split()[0].split("-to-"))
        elif not line:
            continue  # end of current map data
        else:
            # bulk of the processing is here
            destination_range_start, source_range_start, range_length = [
                int(i) for i in line.split()
            ]
            mappings_by_type[current_map].append(
                (destination_range_start, source_range_start, range_length)
            )

    # TODO: we need to cut down the problem space somehow...
    # TODO: work in terms of "ranges" instead of individual numbers
    # ... i.e. if seed range (23, 45) maps to location ranges [(145, 201), (204, 207)]
    # ... then the answer is the minimum of the location ranges

    soil_ranges = do_range_lookup(seed_ranges, mappings_by_type[("seed", "soil")])

    fertilizer_ranges = do_range_lookup(
        soil_ranges, mappings_by_type[("soil", "fertilizer")]
    )

    water_ranges = do_range_lookup(
        fertilizer_ranges, mappings_by_type[("fertilizer", "water")]
    )

    light_ranges = do_range_lookup(water_ranges, mappings_by_type[("water", "light")])

    temperature_ranges = do_range_lookup(
        light_ranges, mappings_by_type[("light", "temperature")]
    )

    humidity_ranges = do_range_lookup(
        temperature_ranges, mappings_by_type[("temperature", "humidity")]
    )

    location_ranges = do_range_lookup(
        humidity_ranges, mappings_by_type[("humidity", "location")]
    )

    for location_range in location_ranges:
        low, high = location_range
        # go in reverse to verify that this location can be gotten to by a seed? no, that shouldn't be necessary...

    print(sorted(location_ranges)[:3])
    return str(min(location_ranges)[0])


def do_range_lookup(source_ranges: list[tuple], mappings: list[tuple]) -> list[tuple]:
    destination_ranges: list[range] = []

    # [ ((source range), (dest range)) ]
    range_mappings: list[tuple[tuple, tuple]] = []
    for mapping in mappings:
        (
            destination_range_mapping_start,
            source_range_mapping_start,
            range_length,
        ) = mapping
        source_mapping_range = (
            source_range_mapping_start,
            source_range_mapping_start + range_length,
        )
        destination_mapping_range = (
            destination_range_mapping_start,
            destination_range_mapping_start + range_length,
        )
        range_mappings.append((source_mapping_range, destination_mapping_range))

    for source_range in source_ranges:
        applicable_range_mappings = [
            m for m in range_mappings if overlaps(source_range, m[0])
        ]

        if not applicable_range_mappings:
            destination_ranges.append(source_range)

        for mapping in applicable_range_mappings:
            # ranges are EXCLUSIVE of the high number i.e. (1, 5) is [ 1, 2, 3, 4 ]
            # get below (if any)
            if source_range[0] < mapping[0][0]:
                below = (source_range[0], mapping[0][0])
                destination_ranges.append(below)
            # get above (if any)
            if source_range[1] - 1 > mapping[0][1] - 1:
                above = (
                    mapping[0][1] - 1,
                    source_range[1] - 1,
                )
                destination_ranges.append(above)
            # get overlap (if any)
            overlap = (
                max(source_range[0], mapping[0][0]),
                min(source_range[1] - 1, mapping[0][-1] - 1),
            )
            if overlap[1] >= overlap[0]:
                difference = mapping[1][0] - mapping[0][0]
                dest_overlap = (overlap[0] + difference, overlap[1] + difference - 1)
                destination_ranges.append(dest_overlap)

    return destination_ranges


def overlaps(a: tuple, b: tuple) -> bool:
    # print(f"Computing overlap between {a} and {b}")
    return a[0] <= b[1] - 1 and b[0] <= a[1] - 1


def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


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
