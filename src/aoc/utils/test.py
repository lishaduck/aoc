from pathlib import Path
from typing import Any

from aocd.types import PuzzlePart
import rich

from aoc.base import BaseSolution, Output


def answer(
    day: int,
    part: PuzzlePart,
    day_dir: Path,
    tested: BaseSolution[Any, Any],
) -> Output | None:
    in_file: Path = day_dir / f"{day:0>2}.in"
    input_content = in_file.read_text(encoding="utf-8")

    answer = tested.run(input_content, part=part)

    rich.print(answer)
    assert answer

    return str(answer)


def snapshot(
    day: int,
    part: PuzzlePart,
    day_dir: Path,
) -> str:
    out_file: Path = day_dir / f"{day:0>2}{part}.out"

    output_snapshot = out_file.read_text(encoding="utf-8")

    assert output_snapshot

    return output_snapshot
