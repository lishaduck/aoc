from collections.abc import Iterable
from dataclasses import dataclass
import enum
from enum import Enum
import functools
import re
from typing import override

from aoc.base import AoCError, StringSolution


@dataclass
class Handful:
    red: int
    green: int
    blue: int


class Color(Enum):
    red = enum.auto()
    green = enum.auto()
    blue = enum.auto()


red_regex = re.compile("\\d red")
green_regex = re.compile("\\d green")
blue_regex = re.compile("\\d blue")


def color_of_cube_set(cube_set: str) -> tuple[Color, int]:
    red_match = red_regex.match(cube_set)
    green_match = green_regex.match(cube_set)
    blue_match = blue_regex.match(cube_set)

    if red_match is not None:
        return (Color.red, red_match.start())

    if green_match is not None:
        return (Color.green, green_match.start())

    if blue_match is not None:
        return (Color.blue, blue_match.start())

    raise AoCError


def total_color(parsed_cube_set: Iterable[tuple[Color, int]], color: Color) -> int:
    def reducer(acc: int, new: tuple[Color, int]) -> int:
        return acc + new[1] if new[0] == color else acc

    return functools.reduce(reducer, parsed_cube_set, 0)


class Solution(StringSolution[list[list[Handful]]]):
    @override
    def transform(self, values: str) -> list[list[Handful]]:
        """Convert string into a list of rounds consisting of a list of handfuls."""

        return [
            ([
                Handful(
                    total_color(parsed_cube_set, Color.red),
                    total_color(parsed_cube_set, Color.green),
                    total_color(parsed_cube_set, Color.blue),
                )
                for parsed_cube_set in [
                    [color_of_cube_set(cube_set) for cube_set in handful.split(",")]
                    for handful in game.split(";")
                    if not game.startswith("Game")
                ]
            ])
            for game in values.splitlines()
        ]

    @override
    def part1(self, transformed: list[list[Handful]]) -> int:
        def has_enough_reducer(acc: bool, new: Handful) -> bool:  # noqa: FBT001
            return acc and new.red > 12 and new.green > 13 and new.blue > 14

        a = [functools.reduce(has_enough_reducer, game, True) for game in transformed]  # noqa: FBT003

        total = 0
        for i in range(len(a)):
            total += i

        return total

    @override
    def part2(self, transformed: list[list[Handful]]) -> None:
        pass  # TODO: solve part 2.
