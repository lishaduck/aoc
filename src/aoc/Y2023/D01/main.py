from typing import override

from aoc.base import BaseSolution


class Solution(BaseSolution[list[str]]):
    @override
    def parse(self, values: str) -> list[str]:
        return values.splitlines()

    @override
    def part1(self, parsed: list[str]) -> int:
        total = 0
        for line in parsed:
            numberline = [int(col) for col in line if col.isdigit()]
            digits: list[int | None] = [None, None]
            for col in numberline:
                if (digits[0]) is None:
                    digits[0] = col
                else:
                    digits[1] = col
            if (digits[1]) is None:
                digits[1] = digits[0]
            assert digits[0] is not None
            assert digits[1] is not None
            total += (digits[0] * 10) + digits[1]
        return total

    @override
    def part2(self, parsed: list[str]) -> int:
        content = [
            values.replace("one", "one1one")
            .replace("two", "two2two")
            .replace("three", "three3three")
            .replace("four", "four4four")
            .replace("five", "five5five")
            .replace("six", "six6six")
            .replace("seven", "seven7seven")
            .replace("eight", "eight8eight")
            .replace("nine", "nine9nine")
            for values in parsed
        ]

        return self.part1(content)
