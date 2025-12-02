from typing import Literal, cast, override

from aoc.base import LinesSolution

type Transformed = list[tuple[Direction, int]]
type Direction = Literal["L", "R"]


class Solution(LinesSolution[Transformed]):
    @override
    def transform(self, values: list[str]) -> Transformed:
        return [
            (cast("Direction", direction), int("".join(distance)))
            for (direction, *distance) in values
        ]

    @override
    def part1(self, rotations: Transformed) -> int:
        pos = 50
        zeros = 0

        for direction, distance in rotations:
            match direction:
                case "L":
                    pos -= distance
                case "R":
                    pos += distance

            while pos >= 100:
                pos -= 100
            while pos < 0:
                pos += 100

            if pos == 0:
                zeros += 1

        return zeros

    @override
    def part2(self, rotations: Transformed) -> int:
        pos = 50
        zeros = 0

        for direction, distance in rotations:
            match direction:
                case "L":
                    pos -= distance

                    if pos == 0:
                        zeros += 1

                    while pos < 0:
                        zeros += 1
                        pos += 100
                case "R":
                    pos += distance

                    while pos >= 100:
                        zeros += 1
                        pos -= 100

        return zeros
