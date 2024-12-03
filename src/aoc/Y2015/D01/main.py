from typing import override

from aoc.base import AoCError, StringSolution


class Solution(StringSolution):
    @override
    def part1(self, parsed: str) -> int:
        floor = 0

        for char in parsed:
            match char:
                case "(":
                    floor += 1
                case ")":
                    floor -= 1
                case _:
                    continue

        return floor

    @override
    def part2(self, parsed: str) -> int:
        floor = 0

        for i, char in enumerate(parsed):
            match char:
                case "(":
                    floor += 1
                case ")":
                    floor -= 1
                case _:
                    continue

            if floor < 0:
                return i + 1

        raise AoCError
