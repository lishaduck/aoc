from enum import StrEnum
import types
from typing import override

import rich

from aoc.base import LinesSolution

consts = types.SimpleNamespace()

empty_mark = "."
boundary_mark = "#"
obstacle_mark = "O"
blockades = {obstacle_mark, boundary_mark}


class Direction(StrEnum):
    left_mark = "<"
    right_mark = ">"
    up_mark = "^"
    down_mark = "V"

    def __repr__(self) -> str:
        return f"'{self}'"


directions = set(Direction)


class Traversed(StrEnum):
    vertical = "|"
    horizontal = "-"
    both = "+"

    def __repr__(self) -> str:
        return f"'{self}'"


traversed = set(Traversed)


def get_pos(grid: list[list[Direction]]) -> tuple[int, int, Direction] | None:
    for iline, line in enumerate(grid):
        for icol, col in enumerate(line):
            if col in directions:
                return (icol, iline, col)

    return None


def walk_path(input_grid: list[list[str]]) -> list[list[str]] | None:  # noqa: C901, PLR0912, PLR0915
    grid = [row[:] for row in input_grid]

    turning = False

    while True:
        pos = get_pos(grid)  # pyright: ignore[reportArgumentType]
        if pos is None:
            break
        x, y, direction = pos

        match direction:
            case Direction.left_mark:
                grid[y][x] = Traversed.horizontal if not turning else Traversed.both
                turning = False
                if x - 1 >= 0:
                    if grid[y][x - 1] in blockades:
                        turning = True
                        grid[y][x] = Direction.up_mark
                    elif grid[y][x - 1] in {Traversed.both, Traversed.horizontal}:
                        rich.print(grid)
                        return None
                    else:
                        grid[y][x - 1] = Direction.left_mark

            case Direction.up_mark:
                grid[y][x] = Traversed.vertical if not turning else Traversed.both
                turning = False
                if y - 1 >= 0:
                    if grid[y - 1][x] in blockades:
                        turning = True
                        grid[y][x] = Direction.right_mark
                    elif grid[y - 1][x] in {Traversed.both, Traversed.vertical}:
                        rich.print(grid)
                        return None
                    else:
                        grid[y - 1][x] = Direction.up_mark

            case Direction.right_mark:
                grid[y][x] = Traversed.horizontal if not turning else Traversed.both
                turning = False
                if x + 1 < len(grid[0]):
                    if grid[y][x + 1] in blockades:
                        turning = True
                        grid[y][x] = Direction.down_mark
                    elif grid[y][x + 1] in {Traversed.both, Traversed.horizontal}:
                        rich.print(grid)
                        return None
                    else:
                        grid[y][x + 1] = Direction.right_mark

            case Direction.down_mark:
                grid[y][x] = Traversed.vertical if not turning else Traversed.both
                turning = False
                if y + 1 < len(grid):
                    if grid[y + 1][x] in blockades:
                        turning = True
                        grid[y][x] = Direction.left_mark
                    elif grid[y + 1][x] in {Traversed.both, Traversed.vertical}:
                        rich.print(grid)
                        return None
                    else:
                        grid[y + 1][x] = Direction.down_mark

    return grid


class Solution(LinesSolution[list[list[str]]]):
    @override
    def transform(self, values: list[str]) -> list[list[str]]:
        return [list(col) for col in values]

    @override
    def part1(self, transformed: list[list[str]]) -> int:
        grid = walk_path(transformed)
        assert grid is not None
        stringified_grid = "".join([y for x in grid for y in x])
        return sum(stringified_grid.count(mark) for mark in traversed)

    @override
    def part2(self, transformed: list[list[str]]) -> int:
        loops = 0

        for y, line in enumerate(transformed):
            for x, col in enumerate(line):
                if col == empty_mark:
                    blocked_grid = [row[:] for row in transformed]
                    blocked_grid[y][x] = "O"
                    grid = walk_path(blocked_grid)
                    stuck_in_loop = grid is None
                    if stuck_in_loop:
                        loops += 1

        return loops
