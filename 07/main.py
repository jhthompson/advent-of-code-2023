from collections import Counter
from enum import Enum
from functools import total_ordering
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


CARD_RANKING = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
WILD_CARD_RANKING = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


@total_ordering
class HandType(Enum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def solve_part_1(input_lines: list[str]) -> str:
    sorted_by_rank = sort_by_rank(input_lines)
    total_winnings = 0

    for index, line in enumerate(sorted_by_rank):
        _, bid = line.split()
        bid = int(bid)

        total_winnings += bid * (1 + index)

    return str(total_winnings)


def sort_by_rank(lines: list[str]):
    decorated = [
        (
            get_hand_strength(line),
            get_card_strength(line[0]),
            get_card_strength(line[1]),
            get_card_strength(line[2]),
            get_card_strength(line[3]),
            get_card_strength(line[4]),
            line,
        )
        for line in lines
    ]
    decorated.sort(reverse=True)

    return [line for _, _, _, _, _, _, line in decorated]


def get_hand_strength(line: str):
    hand, _ = line.split()
    return get_hand_type(hand)


def get_hand_type(hand: str) -> HandType:
    counts = Counter(hand)

    most_common = counts.most_common()

    if most_common[0][1] == 5:
        return HandType.FIVE_OF_A_KIND

    if most_common[0][1] == 4:
        return HandType.FOUR_OF_A_KIND

    if most_common[0][1] == 3:
        if most_common[1][1] == 2:
            return HandType.FULL_HOUSE
        else:
            return HandType.THREE_OF_A_KIND

    if most_common[0][1] == 2:
        if most_common[1][1] == 2:
            return HandType.TWO_PAIR
        else:
            return HandType.ONE_PAIR

    return HandType.HIGH_CARD


def get_wild_card_hand_strength(line: str):
    hand, _ = line.split()
    return get_wild_card_hand_type(hand)


def get_wild_card_hand_type(hand: str) -> HandType:
    counts = Counter(hand)

    most_common = counts.most_common()
    most_common_normal_cards = [count for count in most_common if count[0] != "J"]
    wildcard_count = counts.get("J") or 0

    if most_common[0][1] == 5:
        return HandType.FIVE_OF_A_KIND

    if most_common_normal_cards[0][1] == 4:
        if wildcard_count == 1:
            return HandType.FIVE_OF_A_KIND

        return HandType.FOUR_OF_A_KIND

    if most_common_normal_cards[0][1] == 3:
        if wildcard_count == 2:
            return HandType.FIVE_OF_A_KIND

        if wildcard_count == 1:
            return HandType.FOUR_OF_A_KIND

        if most_common_normal_cards[1][1] == 2:
            return HandType.FULL_HOUSE

        return HandType.THREE_OF_A_KIND

    if most_common_normal_cards[0][1] == 2:
        if wildcard_count == 3:
            return HandType.FIVE_OF_A_KIND

        if wildcard_count == 2:
            return HandType.FOUR_OF_A_KIND

        if most_common_normal_cards[1][1] == 2:
            if wildcard_count == 1:
                return HandType.FULL_HOUSE

            return HandType.TWO_PAIR

        if most_common_normal_cards[1][1] == 1:
            if wildcard_count == 1:
                return HandType.THREE_OF_A_KIND

        return HandType.ONE_PAIR

    if most_common_normal_cards[0][1] == 1:
        if wildcard_count == 4:
            return HandType.FIVE_OF_A_KIND
        if wildcard_count == 3:
            return HandType.FOUR_OF_A_KIND
        if wildcard_count == 2:
            return HandType.THREE_OF_A_KIND
        if wildcard_count == 1:
            return HandType.ONE_PAIR

        return HandType.HIGH_CARD

    return HandType.HIGH_CARD


def get_card_strength(card: str):
    return CARD_RANKING.index(card)


def sort_by_wild_card_rank(lines: list[str]):
    decorated = [
        (
            get_wild_card_hand_strength(line),
            get_wild_card_strength(line[0]),
            get_wild_card_strength(line[1]),
            get_wild_card_strength(line[2]),
            get_wild_card_strength(line[3]),
            get_wild_card_strength(line[4]),
            line,
        )
        for line in lines
    ]
    decorated.sort(reverse=True)

    return [line for _, _, _, _, _, _, line in decorated]


def get_wild_card_strength(card: str):
    return WILD_CARD_RANKING.index(card)


def solve_part_2(input_lines: list[str]) -> str:
    sorted_by_rank = sort_by_wild_card_rank(input_lines)
    total_winnings = 0

    for index, line in enumerate(sorted_by_rank):
        _, bid = line.split()
        bid = int(bid)

        total_winnings += bid * (1 + index)

    return str(total_winnings)


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
