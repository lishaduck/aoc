from __future__ import annotations

from enum import StrEnum
import types
from typing import override

import rich

from aoc.base import LinesSolution

consts = types.SimpleNamespace()

traversed_mark = "X"
boundary = "#"


class Direction(StrEnum):
    left_mark = "<"
    right_mark = ">"
    up_mark = "^"
    down_mark = "V"


def get_pos(parsed: list[list[str]]) -> tuple[int, int, Direction] | None:
    for iline, line in enumerate(parsed):
        for icol, col in enumerate(line):
            if col in set(Direction):
                return (icol, iline, col)

    return None


class Solution(LinesSolution[list[list[str]]]):
    @override
    def transform(self, values: list[str]) -> list[list[str]]:
        return [list(col) for col in values]

    @override
    def part1(self, parsed: list[list[str]]) -> int:
        grid = parsed

        while True:
            pos = get_pos(grid)
            if pos is None:
                break
            x, y, direction = pos

            grid[y][x] = traversed_mark

            match direction:
                case Direction.left_mark:
                    if x - 1 >= 0:
                        if grid[y][x - 1] == boundary:
                            grid[y][x] = Direction.up_mark
                        else:
                            grid[y][x - 1] = Direction.left_mark
                case Direction.up_mark:
                    if y - 1 >= 0:
                        if grid[y - 1][x] == boundary:
                            grid[y][x] = Direction.right_mark
                        else:
                            grid[y - 1][x] = Direction.up_mark
                case Direction.right_mark:
                    if x + 1 < len(grid):
                        if grid[y][x + 1] == boundary:
                            grid[y][x] = Direction.down_mark
                        else:
                            grid[y][x + 1] = Direction.right_mark
                case Direction.down_mark:
                    if y + 1 < len(grid):
                        if grid[y + 1][x] == boundary:
                            grid[y][x] = Direction.left_mark
                        else:
                            grid[y + 1][x] = Direction.down_mark

        rich.print(grid)
        return "".join([y for x in grid for y in x]).count(traversed_mark)

    @override
    def part2(self, parsed: list[list[str]]) -> int:
        pass
