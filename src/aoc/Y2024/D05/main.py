from typing import cast, override

from aoc.base import StringSolution

type Transformed = tuple[Rules, Updates]
type Rules = list[tuple[int, int]]
type Updates = list[Update]
type Update = list[int]


def check_update(update: Update, rules: Rules) -> bool:
    for rule in rules:
        for i, item2 in enumerate(update):
            for item1 in update[:i]:
                if (
                    item1 in rule
                    and item2 in rule
                    and not (item1 == rule[0] or item2 == rule[1])
                ):
                    return False

    return True


class Solution(StringSolution[Transformed]):
    @override
    def transform(self, values: str) -> Transformed:
        rules, nums = values.split("\n\n")

        parsed_rules: list[tuple[int, int]] = [
            cast(tuple[int, int], tuple(int(bound) for bound in rule.split("|"))[:2])
            for rule in rules.splitlines()
        ]
        parsed_nums = [[int(x) for x in x.split(",")] for x in nums.splitlines()]

        return (parsed_rules, parsed_nums)

    @override
    def part1(self, parsed: Transformed) -> int:
        rules, updates = parsed

        good_updates: Updates = []

        for update in updates:
            if check_update(update, rules):
                good_updates.append(update)

        return sum(x[len(x) // 2] for x in good_updates)

    @override
    def part2(self, parsed: Transformed) -> int:
        pass
