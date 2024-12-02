import re
from typing import override

from aoc.base import BaseSolution


class Solution(BaseSolution[list[list[int]]]):
    @override
    def parse(self, values: str) -> list[list[int]]:
        matches: list[list[str]] = [re.findall(r"\d+", x) for x in values.splitlines()]

        return [[int(num) for num in line] for line in matches]

    @override
    def part1(self, parsed: list[list[int]]) -> int:
        a = sorted([x[0] for x in parsed])
        b = sorted([x[1] for x in parsed])

        return sum(abs(ai - bi) for ai, bi in zip(a, b, strict=True))

    @override
    def part2(self, parsed: list[list[int]]) -> int:
        a = [x[0] for x in parsed]
        b = [x[1] for x in parsed]
        similar_totals = [ax * b.count(ax) for ax in a]

        return sum(similar_totals)
