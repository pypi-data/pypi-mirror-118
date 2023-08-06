from dataclasses import dataclass
from typing import Iterable, List, Optional

from .lines import Line
from .syntax import NULL_SYMBOL


@dataclass
class Pos:
    """Line number and column position.
    These numbers starts from Zero.
    """

    line: int
    ch: int

    def __eq__(self, other) -> bool:
        return self.line == other.line and self.ch == other.ch

    def __repr__(self) -> str:
        return f"Pos({self.line}, {self.ch})"


@dataclass
class Paragraph:
    number: int
    lines: List[Line]
    is_head: bool = False
    is_list: bool = False
    _body: Optional[str] = None

    def __eq__(self, other):
        return (
            self.number == other.number
            and self.lines == other.lines
            and self.is_head is other.is_head
            and self.is_list is other.is_list
        )

    @property
    def body(self):
        if self._body is not None:
            return self._body
        self._body = "\n".join(line.body.strip().replace(NULL_SYMBOL, "") for line in self.lines)
        return self._body

    def as_original_pos(self, index) -> Pos:
        before_lines = self.body[:index].split("\n")
        pos = Pos(
            len(before_lines) - 1,
            len(before_lines[-1]),
        )
        # Convert column number to original position.
        line = self.lines[pos.line].body
        left_margin = len(line) - len(line.lstrip())
        chunks = line[left_margin:].split(NULL_SYMBOL)
        num_null_symbols = 0
        current = 0
        for num_null_symbols, chunk in enumerate(chunks):
            current += len(chunk)
            if pos.ch < current:
                break
        pos.line += self.number
        pos.ch += left_margin + num_null_symbols
        return pos

    def __str__(self) -> str:
        return self.body

    def __repr__(self) -> str:
        body = self.body
        if self.is_head:
            body = "# " + body
        elif self.is_list:
            body = "* " + body
        return f"Paragraph({self.number}. {body})"


def parse_paragraph(lines: Iterable[Optional[Line]]) -> Iterable[Paragraph]:
    """
    Combine multiple lines into one Paragraph.
    Each paragraphs has chunks.
    """
    n: int = 0
    p: List[Line] = []
    for i, line in enumerate(lines):
        if line is None:
            if p:
                yield Paragraph(n, p)
                p = []
            n = i + 1
            continue

        if line.is_head or line.is_list:
            if p:
                yield Paragraph(n, p)
                p = []
            n = i + 1
            yield Paragraph(
                i,
                [line],
                is_head=line.is_head,
                is_list=line.is_list,
            )
        else:
            p.append(line)
    if p:
        yield Paragraph(n, p)
