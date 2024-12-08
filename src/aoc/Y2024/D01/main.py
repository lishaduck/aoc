import re
from typing import override

from aoc.base import LinesSolution


class Solution(LinesSolution[list[list[int]]]):
    @override
    def transform(self, values: list[str]) -> list[list[int]]:
        matches: list[list[str]] = [re.findall(r"\d+", line) for line in values]

        return [[int(num) for num in line] for line in matches]

    @override
    def part1(self, transformed: list[list[int]]) -> int:
        a = sorted([x[0] for x in transformed])
        b = sorted([x[1] for x in transformed])

        return sum(abs(ai - bi) for ai, bi in zip(a, b, strict=True))

    @override
    def part2(self, transformed: list[list[int]]) -> int:
        a = [x[0] for x in transformed]
        b = [x[1] for x in transformed]
        similar_totals = [ax * b.count(ax) for ax in a]

        return sum(similar_totals)
