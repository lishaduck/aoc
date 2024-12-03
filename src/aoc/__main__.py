import datetime
import importlib
from pathlib import Path
from time import sleep
from typing import Annotated, Any, cast

import aocd
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
import typer
from urllib3.exceptions import MaxRetryError

from aoc.base import BaseSolution

app = typer.Typer(no_args_is_help=True)


p: Path = Path(__file__).resolve().parent


# Eric runs things based on EST.
est = datetime.timezone(datetime.timedelta(hours=-4))
now = datetime.datetime.now(tz=est)

is_december = now.month == 12
is_christmas = is_december and now.day == 25
active_year = now.year if is_december else now.year - 1
active_day = now.day if is_december else 1


@app.command()
def scaffold(
    day: Annotated[
        int,
        typer.Argument(show_default="Today"),
    ] = active_day,
    year: Annotated[
        int,
        typer.Option(show_default=f"{now:%Y}", prompt=""),
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
        try:
            data = aocd.get_data(day=day, year=year)
        except MaxRetryError:
            progress.update(download_task, description="Download failed")
            sleep(0.5)

            data = ""
        progress.remove_task(task_id=download_task)

        progress.add_task(description="Writing data...", total=None)

        day_folder.mkdir(parents=True, exist_ok=True)

        if not main_file.exists():
            main_file.write_text(f"""from typing import override

from aoc.base import BaseSolution


class Solution(BaseSolution[str]):
    @override
    def parse(self, values: str) -> str:
        return values

    @override
    def part1(self, parsed: str) -> int:
        pass

    @override
    def part2(self, parsed: str) -> int:
        {"pass" if not is_christmas else "return None"}
""")
        if not test_file.exists():
            test_file.write_text('""\n')

        init_year_file.write_text(f'"""AoC problems for {year}."""\n')
        init_day_file.write_text(f'""""Day {day} problem for AoC {year}."""\n')
        in_file.write_text(data)
        out_file_a.touch()
        if day != 25:
            out_file_b.touch()


@app.command()
def run(
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

    puzzle_input = in_file.read_text(encoding="utf-8")

    ans1, ans2 = solve(day=day, year=year, data=puzzle_input)

    if ans1 is not None:
        out_file_a.write_text(ans1)
    if ans2 is not None:
        out_file_b.write_text(ans2)

    rich.print(f"Part a: {ans1}\nPart b: {ans2}")


def coerce_solution(solution: str | int | None) -> None | str:
    match solution:
        case None:
            return None
        case str():
            return solution
        case int():
            return str(solution)


def solve(*, year: int, day: int, data: str) -> tuple[str | None, str | None]:
    mod = importlib.import_module(f"aoc.Y{year}.D{day:0>2}.main")

    solution = cast(BaseSolution[Any], mod.Solution())

    parsed = solution.parse(data)
    part1 = solution.part1(parsed)
    part2 = solution.part2(parsed)

    return (coerce_solution(part1), coerce_solution(part2))


def main() -> None:
    app()
