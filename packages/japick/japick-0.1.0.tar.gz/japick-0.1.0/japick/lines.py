from dataclasses import dataclass
from typing import Iterable, Optional

from .syntax import FENCE_END, FENCE_START, HEAD_REGEX, JA_REGEX, LIST_REGEX


class IgnoreBlock:
    def __init__(self):
        self.inside = False
        self.start_regex = FENCE_START
        self.end_regex = FENCE_END

    def should_ignore(self, line: str) -> bool:
        if self.inside:
            if self.end_regex.search(line):
                self.inside = False
            return True
        else:
            if self.start_regex.search(line):
                self.inside = True
                return True
            else:
                return False


@dataclass
class Line:
    body: str
    is_head: bool = False
    is_list: bool = False

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        return (
            self.body == other.body
            and self.is_head is other.is_head
            and self.is_list is other.is_list
        )


def parse_lines(body: str) -> Iterable[Optional[Line]]:
    lines = body.splitlines()
    is_ignore = IgnoreBlock()

    for line in lines:
        if is_ignore.should_ignore(line):
            yield None
        elif JA_REGEX.search(line) is None:
            yield None
        elif HEAD_REGEX.search(line):
            yield Line(line, is_head=True)
        elif LIST_REGEX.search(line):
            yield Line(line, is_list=True)
        else:
            yield Line(line)
