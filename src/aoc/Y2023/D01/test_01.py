from pathlib import Path

from aocd.utils import coerce
import pytest

from aoc.Y2023.D01.main import Solution

p: Path = Path(__file__).resolve().parent

in_file: Path = p / "01.in"


class TestSolution:
    tested = Solution()

    def test_example1(self) -> None:
        example1 = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
        answer1 = 142

        answer = self.tested.run(example1, part=1)
        assert answer == answer1

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
        out_file: Path = p / "01a.out"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=1)

        assert coerce(answer) == output_snapshot

    @pytest.mark.xfail
    def test_snapshot2(self) -> None:
        out_file: Path = p / "01b.out"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=2)

        assert coerce(answer) == output_snapshot
