from pathlib import Path

from aocd.utils import coerce
import pytest

from aoc.Y2015.D01.main import Solution

p: Path = Path(__file__).resolve().parent

in_file: Path = p / "01.in"


class TestSolution:
    tested = Solution()

    @pytest.mark.parametrize(
        ("example", "example_answer"),
        [
            ("""(())""", 0),
            ("""()()""", 0),
            ("""(((""", 3),
            ("""(()(()(""", 3),
            ("""))(((((""", 3),
            ("""())""", -1),
            ("""))(""", -1),
            (""")))""", -3),
            (""")())())""", -3),
        ],
    )
    def test_example1(self, example: str, example_answer: int) -> None:
        answer = self.tested.run(example, part=1)
        assert answer == example_answer

    @pytest.mark.parametrize(
        ("example", "example_answer"),
        [
            (""")""", 1),
            ("""()())""", 5),
        ],
    )
    def test_example2(self, example: str, example_answer: int) -> None:
        answer = self.tested.run(example, part=2)
        assert answer == example_answer

    def test_snapshot1(self) -> None:
        out_file: Path = p / "01a.out"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=1)

        assert coerce(answer) == output_snapshot

    def test_snapshot2(self) -> None:
        out_file: Path = p / "01b.out"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=2)

        assert coerce(answer) == output_snapshot
