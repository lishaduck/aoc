from abc import ABC, abstractmethod
from typing import Literal

type Output = str | int


class BaseSolution[Parsed](ABC):
    @abstractmethod
    def parse(self, values: str) -> Parsed: ...

    @abstractmethod
    def part1(self, parsed: Parsed) -> Output: ...

    @abstractmethod
    def part2(self, parsed: Parsed) -> Output | None:  # Christmas day has no Part 2.
        ...

    def run(self, values: str, *, part: Literal[1, 2]) -> Output | None:
        parsed = self.parse(values)

        match part:
            case 1:
                return self.part1(parsed)
            case 2:
                return self.part2(parsed)
