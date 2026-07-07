from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class SectionAssignment:
    start: int
    end: int

    def overlaps(self, other: SectionAssignment) -> bool:
        if self.end < other.start or other.end < self.start:
            return False

        return True


def parse(filename: str) -> List[Tuple[SectionAssignment, SectionAssignment]]:
    with open(filename, "r") as fp:
        lines: List[str] = fp.read().splitlines()

    section_assignments: List[Tuple[SectionAssignment, SectionAssignment]] = []

    for pair in lines:
        first_pair, second_pair = pair.split(",")
        first_init, first_end = first_pair.split("-")
        second_init, second_end = second_pair.split("-")

        section_assignments.append(
            (
                SectionAssignment(int(first_init), int(first_end)),
                SectionAssignment(int(second_init), int(second_end)),
            )
        )

    return section_assignments


def solve(
    section_assignments: List[Tuple[SectionAssignment, SectionAssignment]],
) -> int:
    total_overlaps: int = 0

    for section_assignment in section_assignments:
        first_section, second_section = section_assignment

        if first_section.overlaps(second_section):
            total_overlaps += 1

    return total_overlaps


def solution(filename: str) -> int:
    section_assignments = parse(filename)
    return solve(section_assignments)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 4
    print(solution("./input.txt"))  # 830
