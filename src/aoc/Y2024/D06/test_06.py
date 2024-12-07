from pathlib import Path

import pytest

from aoc.Y2024.D06.main import Solution

p: Path = Path(__file__).resolve().parent

in_file: Path = p / "06.in"


class TestSolution:
    tested = Solution()

    @pytest.mark.parametrize(
        ("example", "example_answer"),
        [
            (
                """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""",
                41,
            ),
        ],
    )
    def test_example1(self, example: str, example_answer: int) -> None:
        answer = self.tested.run(example, part=1)
        assert answer == example_answer

    @pytest.mark.parametrize(
        ("example", "example_answer"),
        [
            (
                """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""",
                6,
            ),
        ],
    )
    def test_example2(self, example: str, example_answer: int) -> None:
        answer = self.tested.run(example, part=2)

        assert answer == example_answer

    def test_snapshot1(self) -> None:
        out_file: Path = p / "06a.out"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=1)

        assert str(answer) == output_snapshot

    @pytest.mark.xfail
    def test_snapshot2(self) -> None:
        out_file: Path = p / "06b.out"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=2)

        assert str(answer) == output_snapshot
