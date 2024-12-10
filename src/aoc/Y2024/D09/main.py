from typing import override

from aoc.base import AoCError, StringSolution

type Fs = list[int | None]


def get_empty_index(fs: Fs, size: int = 1) -> int | None:
    found = 0

    for i, file in enumerate(fs):
        if file is None:
            found += 1

            if found == size:
                return i - found + 1
        else:
            found = 0

    return None


def compact(old_fs: Fs) -> Fs:
    fs = old_fs[:]

    for i, file in reversed(list(enumerate(fs))):
        next_empty_index = get_empty_index(fs)
        if file is None:
            continue

        if next_empty_index is None or next_empty_index >= i:
            break

        fs[next_empty_index] = file
        fs[i] = None

    return fs


def format_fs(fs: Fs) -> str:
    rep = ""

    for file in fs:
        if file is None:
            rep += "."
        else:
            rep += str(file)

    return rep


def compact_without_fragmenting(old_fs: Fs) -> Fs:
    fs = old_fs[:]

    current: tuple[int, list[int]] = (len(fs), [])

    for i, file in reversed(list(enumerate(fs))):
        if file is None or (len(current[1]) > 0 and file != current[1][0]):
            next_empty_index = get_empty_index(fs, len(current[1]))

            if next_empty_index is None or next_empty_index > i:
                current = (i, [file]) if file is not None else (i, [])
                continue

            for j, file_ in enumerate(current[1]):
                fs[next_empty_index + j] = file_
                fs[(i + 1) + j] = None

            current = (i, [file]) if file is not None else (i, [])
        else:
            current[1].append(file)

    return fs


def calculate_checksum(fs: Fs) -> int:
    file_hashes: list[int] = []

    for i, file_id in enumerate(fs):
        if file_id is None:
            continue

        file_hashes.append(i * file_id)

    return sum(file_hashes)


class Solution(StringSolution[Fs]):
    @override
    def transform(self, values: str) -> Fs:
        blocks: Fs = []
        for i, content in enumerate(values):
            match i % 2:
                case 0:
                    blocks += [(i // 2) for _ in range(int(content))]
                case 1:
                    blocks += [None for _ in range(int(content))]
                case _:
                    raise AoCError
        return blocks

    @override
    def part1(self, fs: Fs) -> int:
        compacted = compact(fs)

        return calculate_checksum(compacted)

    @override
    def part2(self, fs: Fs) -> int:
        compacted = compact_without_fragmenting(fs)

        return calculate_checksum(compacted)
