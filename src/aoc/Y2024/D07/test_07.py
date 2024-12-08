from pathlib import Path

import pytest

from aoc.Y2024.D07.main import Solution

p: Path = Path(__file__).resolve().parent

in_file: Path = p / "07.in"


class TestSolution:
    tested = Solution()

    @pytest.mark.parametrize(
        ("example", "example_answer"),
        [
            (
                """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""",
                3749,
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
                """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""",
                11387,
            ),
        ],
    )
    def test_example2(self, example: str, example_answer: int) -> None:
        answer = self.tested.run(example, part=2)

        assert answer == example_answer

    def test_snapshot1(self) -> None:
        out_file: Path = p / "07a.out"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=1)

        assert str(answer) == output_snapshot

    @pytest.mark.xfail
    def test_snapshot2(self) -> None:
        out_file: Path = p / "07b.out"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=2)

        assert str(answer) == output_snapshot
