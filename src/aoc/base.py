from abc import ABC, abstractmethod
from typing import Literal, override

type Output = str | int


class AoCError(Exception):
    """Base exception for AoC errors."""


class BaseSolution[Parsed, Transformed](ABC):
    @abstractmethod
    def parse(self, values: str) -> Parsed: ...

    def transform(self, values: Parsed) -> Transformed:  # noqa: PLR6301
        return values  # pyright: ignore[reportReturnType]

    @abstractmethod
    def part1(self, transformed: Transformed, /) -> Output: ...

    @abstractmethod
    def part2(
        self,
        transformed: Transformed,
        /,
    ) -> Output | None:  # Christmas day has no Part 2.
        ...

    def run(self, values: str, *, part: Literal[1, 2]) -> Output | None:
        parsed = self.parse(values)
        transformed = self.transform(parsed)

        match part:
            case 1:
                return self.part1(transformed)
            case 2:
                return self.part2(transformed)


class StringSolution[Transformed = str](BaseSolution[str, Transformed]):
    @override
    def parse(self, values: str) -> str:
        return values


class LinesSolution[Transformed = list[str]](BaseSolution[list[str], Transformed]):
    @override
    def parse(self, values: str) -> list[str]:
        return values.splitlines()
