import re
from typing import override

from aoc.base import AoCError, StringSolution


class Solution(StringSolution):
    @override
    def part1(self, parsed: str) -> int:
        inst = re.compile(r"mul\(\d+,\d+\)")
        matches: list[str] = re.findall(inst, parsed)

        transformed = [
            (int(a), int(b))
            for match in matches
            for a, b in [match.removeprefix("mul(").removesuffix(")").split(",")]
        ]

        return sum(p1 * p2 for p1, p2 in transformed)

    @override
    def part2(self, parsed: str) -> int:
        inst = re.compile(r"(?:mul\(\d+,\d+\)|do\(\)|don't\(\))")
        matches: list[str] = re.findall(inst, parsed)
        instructions: list[tuple[int, int]] = []

        splitter = re.compile(r"[\(,]")

        active = True

        for match in matches:
            name, *e = re.split(splitter, match.removesuffix(")"))

            match name:
                case "mul" if active:
                    a, b = e
                    instructions.append((int(a), int(b)))
                case "mul" if not active:
                    pass
                case "do":
                    active = True
                case "don't":
                    active = False
                case _:
                    raise AoCError

        return sum(p1 * p2 for p1, p2 in instructions)
