import datetime
import importlib
from pathlib import Path
from typing import Annotated, Any, cast

import aocd
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
import typer

from aoc.base import BaseSolution

app = typer.Typer(no_args_is_help=True)


p: Path = Path(__file__).resolve().parent


# Eric runs things based on EST.
est = datetime.timezone(datetime.timedelta(hours=-4))
now = datetime.datetime.now(tz=est)

active_year = now.year if now.month == 12 else now.year - 1
active_day = 1


@app.command()
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
    init_year_file: Path = year_folder / "__init__.py"
    init_day_file: Path = day_folder / "__init__.py"

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        download_task = progress.add_task(description="Downloading data...", total=None)
        data = aocd.get_data(day=day, year=year)
        progress.remove_task(task_id=download_task)

        progress.add_task(description="Writing data...", total=None)

        day_folder.mkdir(parents=True, exist_ok=True)
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

    puzzle_input = in_file.read_text()

    ans1, ans2 = solve(day=day, year=year, data=puzzle_input)

    out_file_a.write_text(ans1)

    if ans2 is not None:
        out_file_b.write_text(ans2)

    rich.print(f"Part a: {ans1}\nPart b: {ans2}")


def solve(*, year: int, day: int, data: str) -> tuple[str, str | None]:
    mod = importlib.import_module(f"aoc.Y{year}.D{day:0>2}.main")

    solution = cast(BaseSolution[Any], mod.Solution())

    parsed = solution.parse(data)
    part1 = solution.part1(parsed)
    part2 = solution.part2(parsed)

    return (str(part1), str(part2))


def main() -> None:
    app()
