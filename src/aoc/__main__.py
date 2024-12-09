import datetime
import importlib
from pathlib import Path
from time import sleep
from typing import Annotated, Any, cast

from aocd.models import Puzzle
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
import typer
from urllib3.exceptions import MaxRetryError

from aoc.base import BaseSolution, Output

app = typer.Typer(no_args_is_help=True)


p: Path = Path(__file__).resolve().parent


# Eric runs things based on EST.
est = datetime.timezone(datetime.timedelta(hours=-4))
now = datetime.datetime.now(tz=est)

is_december = now.month == 12
is_christmas = is_december and now.day == 25
active_year = now.year if is_december else now.year - 1
active_day = now.day if is_december else 1


def coercible_to_int(s: str | None) -> bool:
    if s is None:
        return False

    try:
        int(s)
    except ValueError:
        return False
    else:
        return True


@app.command(help="Scaffold out the next puzzle")
def scaffold(
    day: Annotated[
        int,
        typer.Argument(show_default="Today"),
    ] = active_day,
    year: Annotated[
        int,
        typer.Option(show_default=f"{now:%Y}"),
    ] = active_year,
) -> None:
    year_folder: Path = p / f"Y{year}"
    day_folder: Path = year_folder / f"D{day:0>2}"
    in_file: Path = day_folder / f"{day:0>2}.in"
    out_file_a: Path = day_folder / f"{day:0>2}a.out"
    out_file_b: Path = day_folder / f"{day:0>2}b.out"
    main_file: Path = day_folder / "main.py"
    test_file: Path = day_folder / f"test_{day:0>2}.py"
    init_year_file: Path = year_folder / "__init__.py"
    init_day_file: Path = day_folder / "__init__.py"

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        download_task = progress.add_task(description="Downloading data...", total=None)
        puzzle = Puzzle(year=year, day=day)
        try:
            data = puzzle.input_data
        except MaxRetryError:
            progress.update(download_task, description="Download failed")
            sleep(0.5)

            data = ""

        progress.remove_task(task_id=download_task)

        progress.add_task(description="Writing data...", total=None)

        day_folder.mkdir(parents=True, exist_ok=True)

        if not main_file.exists():
            main_file.write_text(f"""from typing import override

from aoc.base import StringSolution


class Solution(StringSolution):
    @override
    def part1(self, transformed: str) -> int:
        pass # TODO: solve part 1

    @override
    def part2(self, transformed: str) -> int:
        {"pass # TODO: solve part 2" if not is_christmas else "return None"}
""")
        if not test_file.exists():
            examples = puzzle.examples
            has_examples = len(examples) > 0

            example_case = (
                f"""@pytest.mark.parametrize(
        ("example", "example_answer"),
        [{
                    "".join([
                        f'''
            (
                """{x.input_data}""",
                {f'"{x.answer_a}"' if not coercible_to_int(x.answer_a) else x.answer_a},
            ),'''
                        for x in examples
                    ])
                }
        ],
    )
    def test_example1(self, example: str, example_answer: int) -> None:
        answer = self.tested.run(example, part=1)
        assert answer == example_answer
"""
                if has_examples
                else ""
            )

            test_file.write_text(f'''from pathlib import Path

import pytest

from aoc.Y{year}.D{day:0>2}.main import Solution

p: Path = Path(__file__).resolve().parent

in_file: Path = p / "{in_file.name}"


class TestSolution:
    tested = Solution()

    {example_case}
    @pytest.mark.xfail
    @pytest.mark.parametrize(
        ("example", "example_answer"),
        [
            (
                """""",
                0,
            ),
        ],
    )
    def test_example2(self, example: str, example_answer: int) -> None:
        answer = self.tested.run(example, part=2)

        assert answer == example_answer

    @pytest.mark.xfail
    def test_snapshot1(self) -> None:
        out_file: Path = p / "{out_file_a.name}"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=1)

        assert str(answer) == output_snapshot

    @pytest.mark.xfail
    def test_snapshot2(self) -> None:
        out_file: Path = p / "{out_file_b.name}"

        input_content = in_file.read_text(encoding="utf-8")
        output_snapshot = out_file.read_text(encoding="utf-8")

        answer = self.tested.run(input_content, part=2)

        assert str(answer) == output_snapshot
''')

        init_year_file.write_text(f'"""AoC problems for {year}."""\n')
        init_day_file.write_text(f'""""Day {day} problem for AoC {year}."""\n')
        in_file.write_text(data)
        out_file_a.touch()
        if day != 25:
            out_file_b.touch()


@app.command(help="Run the solver, save snapshots, submit answers")
def run(
    day: Annotated[
        int,
        typer.Argument(show_default="Today"),
    ] = active_day,
    year: Annotated[
        int,
        typer.Option(show_default=f"{now:%Y}"),
    ] = active_year,
    *,
    write: bool = True,
    submit: bool = False,
) -> None:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        t1 = progress.add_task("Initializing")
        year_folder: Path = p / f"Y{year}"
        day_folder: Path = year_folder / f"D{day:0>2}"
        out_file_a: Path = day_folder / f"{day:0>2}a.out"
        out_file_b: Path = day_folder / f"{day:0>2}b.out"
        puzzle = Puzzle(year=year, day=day)
        progress.remove_task(t1)

        t2 = progress.add_task("Solving")
        ans1, ans2 = solve(puzzle)
        rich.print(f"Part a: {ans1}\nPart b: {ans2}")
        progress.remove_task(t2)

        if ans1 is not None:
            if write:
                t3 = progress.add_task("Saving 1")
                out_file_a.write_text(str(ans1))
                progress.remove_task(t3)

            if submit:
                t4 = progress.add_task("Submitting 1")
                puzzle.answer_a = ans1  # pyright: ignore[reportAttributeAccessIssue]
                progress.remove_task(t4)
        if ans2 is not None:
            if write:
                t3 = progress.add_task("Saving 2")
                out_file_b.write_text(str(ans2))
                progress.remove_task(t3)

            if submit:
                t4 = progress.add_task("Submitting 2")
                puzzle.answer_b = ans2  # pyright: ignore[reportAttributeAccessIssue]
                progress.remove_task(t4)


def solve(puzzle: Puzzle) -> tuple[Output | None, Output | None]:
    mod = importlib.import_module(f"aoc.Y{puzzle.year}.D{puzzle.day:0>2}.main")

    solution = cast(BaseSolution[Any, Any], mod.Solution())

    parsed = solution.parse(puzzle.input_data)
    transformed = solution.transform(parsed)
    part1 = solution.part1(transformed)
    part2 = solution.part2(transformed)

    return (part1, part2)


def main() -> None:
    app()
