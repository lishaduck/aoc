from typing import override

from aoc.base import LinesSolution


class Solution(LinesSolution[list[list[int]]]):
    @override
    def transform(self, values: list[str]) -> list[list[int]]:
        return [[int(col) for col in line.split(" ")] for line in values]

    @override
    def part1(self, transformed: list[list[int]]) -> int:
        safe = 0

        for line in transformed:
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
    def part2(self, transformed: list[list[int]]) -> int:
        safe = 0

        for line in transformed:
            last = 0
            mode = True  # True is up

            for dampening in range(len(line)):
                for i, col in enumerate(line[:dampening] + line[dampening + 1 :]):
                    if i == 1:
                        mode = last < col

                    if (i != 0) and (
                        ((last < col) != mode) or (abs(last - col) > 3) or (last == col)
                    ):
                        break

                    last = col
                else:
                    safe += 1
                    break

        return safe
