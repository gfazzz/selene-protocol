#!/usr/bin/env python3
"""Проверяет маршрут: серии без повторов, оси и зависимости (SPEC.md §1)."""

import re
import sys
from collections import Counter, defaultdict

from route import ROUTE, read_series

ARTIFACTS = {
    1: "toolkit", 2: "toolkit", 3: "intake", 4: "metrics", 5: "contract",
    6: "relay", 7: "gateway", 8: "registry", 9: "oracle", 10: "mind",
    11: "graft", 12: "mesh", 13: "budget", 14: "node", 15: "selene_core",
}


def main():
    series = read_series()
    errors = []
    ids = [row["id"] for row in series]
    text = ROUTE.read_text(encoding="utf-8")
    declared = {
        int(m.group(1)): int(m.group(2))
        for m in re.finditer(r"^\| S(\d+) \|(?:[^|]*\|){3} (\d+) \|", text, re.M)
    }
    expected = [f"s{s:02}e{e:02}" for s in sorted(declared) for e in range(1, declared[s] + 1)]
    if sorted(declared) != list(range(1, 16)):
        errors.append("в таблице сезонов не пятнадцать сезонов с числом серий")
    if ids != expected:
        errors.append("номера серий идут не по порядку или расходятся с таблицей сезонов")

    for column in ("title", "concept", "artifact"):
        for value, count in Counter(row[column] for row in series).items():
            if count > 1:
                errors.append(f"повтор в колонке {column}: {value}")

    axes = defaultdict(Counter)
    for row in series:
        season = int(row["id"][1:3])
        axes[season][row["axis"]] += 1
        if not row["artifact"].strip("`").startswith(ARTIFACTS[season] + "/"):
            errors.append(f"{row['id']}: артефакт не из пакета {ARTIFACTS[season]}")
    for season, counts in sorted(axes.items()):
        if len(counts) < 3:
            errors.append(f"S{season}: меньше трёх осей")
        if max(counts.values()) * 2 > sum(counts.values()):
            errors.append(f"S{season}: одна ось больше чем в половине серий")

    deps = text[text.index("## Зависимости"):text.index("## Что считается")]
    for line in deps.splitlines():
        cells = line.split("|")
        if len(cells) > 3:
            used = re.findall(r"s\d\de\d\d", cells[3])
            for source in re.findall(r"s\d\de\d\d", cells[2]):
                if source not in ids or any(u not in ids or u < source for u in used):
                    errors.append(f"зависимость идёт вперёд: {line}")

    for error in errors:
        print(error)
    if not errors:
        print(f"Маршрут: всё сходится, серий {len(series)}")
    else:
        print(f"Маршрут: ошибок {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
