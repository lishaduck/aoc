from typing import override

from aoc.base import LinesSolution


class Solution(LinesSolution):
    @override
    def part1(self, lines: list[str]) -> int:  # noqa: C901, PLR0912
        count = 0

        height = len(lines)

        for y, line in enumerate(lines):
            width = len(line)

            for x, col in enumerate(line):
                if col == "X":
                    has_up_space = y >= 3
                    has_down_space = y <= height - 4
                    has_left_space = x >= 3
                    has_right_space = x <= width - 4

                    # Vertical

                    if has_down_space and (
                        lines[y + 1][x] == "M"
                        and lines[y + 2][x] == "A"
                        and lines[y + 3][x] == "S"
                    ):
                        count += 1
                    if has_up_space and (
                        lines[y - 1][x] == "M"
                        and lines[y - 2][x] == "A"
                        and lines[y - 3][x] == "S"
                    ):
                        count += 1

                    # Right

                    if has_right_space:
                        if (
                            line[x + 1] == "M"
                            and line[x + 2] == "A"
                            and line[x + 3] == "S"
                        ):
                            count += 1

                        if has_down_space and (
                            lines[y + 1][x + 1] == "M"
                            and lines[y + 2][x + 2] == "A"
                            and lines[y + 3][x + 3] == "S"
                        ):
                            count += 1
                        if has_up_space and (
                            lines[y - 1][x + 1] == "M"
                            and lines[y - 2][x + 2] == "A"
                            and lines[y - 3][x + 3] == "S"
                        ):
                            count += 1

                    # Left

                    if has_left_space:
                        if (
                            line[x - 1] == "M"
                            and line[x - 2] == "A"
                            and line[x - 3] == "S"
                        ):
                            count += 1

                        if has_down_space and (
                            lines[y + 1][x - 1] == "M"
                            and lines[y + 2][x - 2] == "A"
                            and lines[y + 3][x - 3] == "S"
                        ):
                            count += 1
                        if has_up_space and (
                            lines[y - 1][x - 1] == "M"
                            and lines[y - 2][x - 2] == "A"
                            and lines[y - 3][x - 3] == "S"
                        ):
                            count += 1

        return count

    @override
    def part2(self, lines: list[str]) -> int:
        count = 0

        height = len(lines)
        width = len(lines[0]) if height > 0 else 0

        for y, line in enumerate(lines):
            for x, col in enumerate(line):
                if (
                    col == "A"  # noqa: PLR0916
                    and (y > 0 and y < height - 1 and x > 0 and x < width - 1)
                    and (
                        (
                            lines[y - 1][x - 1] == "M"
                            and lines[y - 1][x + 1] == "S"
                            and lines[y + 1][x - 1] == "M"
                            and lines[y + 1][x + 1] == "S"
                        )
                        or (
                            lines[y - 1][x - 1] == "S"
                            and lines[y - 1][x + 1] == "M"
                            and lines[y + 1][x - 1] == "S"
                            and lines[y + 1][x + 1] == "M"
                        )
                        or (
                            lines[y - 1][x - 1] == "M"
                            and lines[y - 1][x + 1] == "M"
                            and lines[y + 1][x - 1] == "S"
                            and lines[y + 1][x + 1] == "S"
                        )
                        or (
                            lines[y - 1][x - 1] == "S"
                            and lines[y - 1][x + 1] == "S"
                            and lines[y + 1][x - 1] == "M"
                            and lines[y + 1][x + 1] == "M"
                        )
                    )
                ):
                    count += 1

        return count
