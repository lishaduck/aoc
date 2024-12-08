from collections.abc import Callable
from itertools import product
from operator import add, mul
from typing import override

from aoc.base import LinesSolution


def concat_num(a: int, b: int) -> int:
    return int(f"{a}{b}")


type OpList = list[Callable[[int, int], int]]
ops: OpList = [mul, add]
ops2: OpList = [mul, add, concat_num]


def calibrate(equations: list[str], operations: OpList) -> int:
    num = 0
    for line in equations:
        ans_, eq = line.split(": ")
        real_ans = int(ans_)
        terms = [int(term) for term in eq.split(" ")]

        for ops_list in product(operations, repeat=len(terms) - 1):
            ans = terms[0]
            for term, op in zip(terms[1:], ops_list, strict=True):
                ans = op(ans, term)

            if ans == real_ans:
                num += real_ans
                break

    return num


class Solution(LinesSolution):
    @override
    def part1(self, parsed: list[str]) -> int:
        return calibrate(parsed, ops)

    @override
    def part2(self, parsed: list[str]) -> int:
        return calibrate(parsed, ops2)
