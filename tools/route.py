"""Чтение docs/ROUTE.md как данных."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "docs" / "ROUTE.md"
COLUMNS = ("id", "title", "concept", "artifact", "axis", "check")


def read_series():
    series = []
    for line in ROUTE.read_text(encoding="utf-8").splitlines():
        if re.match(r"\| s\d\de\d\d \|", line):
            cells = [cell.strip() for cell in line.strip("| \n").split(" | ")]
            if len(cells) != len(COLUMNS):
                raise ValueError(f"В строке не {len(COLUMNS)} колонок: {line}")
            series.append(dict(zip(COLUMNS, cells)))
    return series
