from pathlib import Path

import pytest

from aoc.utils.test import answer, snapshot
from aoc.Y2023.D01.main import Solution

p: Path = Path(__file__).resolve().parent

in_file: Path = p / "01.in"


class TestSolution:
    tested = Solution()

    @pytest.mark.parametrize(
        ("example", "example_answer"),
        [
            (
                """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""",
                142,
            )
        ],
    )
    def test_example1(self, example: str, example_answer: int) -> None:
        answer = self.tested.run(example, part="a")
        assert answer == example_answer

    def test_example2(self) -> None:
        example2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
        answer2 = 281

        answer = self.tested.run(example2, part=2)

        assert answer == answer2

    def test_snapshot1(self) -> None:
        snapshotted = snapshot(day=1, part="a", day_dir=p)
        solved = answer(day=1, part="a", day_dir=p, tested=self.tested)

        assert solved == snapshotted

    @pytest.mark.xfail
    def test_snapshot2(self) -> None:
        snapshotted = snapshot(day=1, part="b", day_dir=p)
        solved = answer(day=1, part="b", day_dir=p, tested=self.tested)

        assert solved == snapshotted
