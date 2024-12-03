from typing import override

from aoc.base import BaseSolution


class Solution(BaseSolution[list[list[int]]]):
    @override
    def parse(self, values: str) -> list[list[int]]:
        return [[int(col) for col in line.split(" ")] for line in values.splitlines()]

    @override
    def part1(self, parsed: list[list[int]]) -> int:
        safe = 0

        for line in parsed:
            last = 0
            mode = True  # True is up

            for i, col in enumerate(line):
                if i == 1:
                    mode = last < col

                if (i != 0) and (
                    ((last < col) != mode) or (abs(last - col) > 3) or (last == col)
                ):
                    safe -= 1
                    break

                last = col

            safe += 1

        return safe

    @override
    def part2(self, parsed: list[list[int]]) -> int:
        safe = 0

        for line in parsed:
            last = 0
            mode = True  # True is up

            dampening = 0

            while dampening < len(line):
                for i, col in enumerate(line[:dampening] + line[dampening + 1 :]):
                    if i == 1:
                        mode = last < col

                    if (i != 0) and (
                        ((last < col) != mode) or (abs(last - col) > 3) or (last == col)
                    ):
                        break

                    last = col
                else:
                    break

                dampening += 1
                continue

            if dampening != len(line):
                safe += 1

        return safe
