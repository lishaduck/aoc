from pathlib import Path

import pytest

from aoc.Y2024.D05.main import Solution

p: Path = Path(__file__).resolve().parent

in_file: Path = p / "05.in"


class TestSolution:
    tested = Solution()

    @pytest.mark.parametrize(
        ("example", "example_answer"),
        [
            (
                """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""",
                143,
            ),
        ],
    )
    def test_example1(self, example: str, example_answer: int) -> None:
        answer = self.tested.run(example, part=1)
        assert answer == example_answer

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        ("example", "example_answer"),
        [
            (
                """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""",
                143,
            ),
        ],
    )
    def test_example2(self, example: str, example_answer: int) -> None:
        answer = self.tested.run(example, part=2)

        assert answer == example_answer

    def test_snapshot1(self) -> None:
        out_file: Path = p / "05a.out"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=1)

        assert str(answer) == output_snapshot

    @pytest.mark.xfail
    def test_snapshot2(self) -> None:
        out_file: Path = p / "05b.out"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=2)

        assert str(answer) == output_snapshot
