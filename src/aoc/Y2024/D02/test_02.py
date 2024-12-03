""

from pathlib import Path

import pytest

from aoc.Y2024.D02.main import Solution

p: Path = Path(__file__).resolve().parent

in_file: Path = p / "02.in"


class TestSolution:
    tested = Solution()

    @pytest.mark.parametrize(
        ("example", "example_answer"),
        [
            (
                """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""",
                2,
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
                """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""",
                4,
            ),
        ],
    )
    def test_example2(self, example: str, example_answer: int) -> None:
        answer = self.tested.run(example, part=2)

        assert answer == example_answer

    def test_snapshot1(self) -> None:
        out_file: Path = p / "02a.out"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=1)

        assert str(answer) == output_snapshot

    def test_snapshot2(self) -> None:
        out_file: Path = p / "02b.out"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=2)

        assert str(answer) == output_snapshot
