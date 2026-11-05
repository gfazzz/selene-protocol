#!/usr/bin/env python3
"""Проверяет стандарт написанных серий (SPEC.md §1, §3).

Для каждой серии:
- эталон зелёный, и два прогона подряд дают один результат;
- каркас красный;
- каждое неверное решение из tests/mutants/ что-то роняет;
- каждую проверку роняет хотя бы одно неверное решение;
- разделы канона на месте и в нужном порядке, объём в пределах;
- шапка совпадает с docs/ROUTE.md.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

from route import ROOT, read_series

SECTIONS = (
    r"Previously", None, r"Чему ты научишься", r"Теория: .+",
    r"Проверка: SELENE задаёт вопросы", r"Задание: `.+`",
    r"Разбор типичных ошибок", r"Debriefing", r"Ссылки и AI-usage", r"Навигация",
)
# Имя проверки может содержать пробелы (параметры), поэтому берём его до « - ».
RESULT = re.compile(r"^(PASSED|FAILED|ERROR) (.+?)(?: - .*)?$", re.M)


def run_tests(series, source):
    env = {**os.environ, "SELENE_SOURCE": str(source)}
    done = subprocess.run(
        [sys.executable, "-m", "pytest", str(series / "tests"), "-q", "--tb=no", "-rA"],
        cwd=ROOT, env=env, capture_output=True, text=True, check=False,
    )
    return {name: status == "PASSED" for status, name in RESULT.findall(done.stdout)}


def check_tests(series):
    errors = []
    first = run_tests(series, "solution")
    if not first or not all(first.values()):
        return [f"эталон не зелёный: {first}"], 0
    if run_tests(series, "solution") != first:
        errors.append("два прогона эталона дали разный результат")
    if all(run_tests(series, "starter").values()):
        errors.append("каркас проходит все проверки")

    mutants = sorted((series / "tests" / "mutants").glob("*.py"))
    if not mutants:
        errors.append("нет неверных решений в tests/mutants/")
    killed = set()
    for mutant in mutants:
        failed = {name for name, ok in run_tests(series, mutant).items() if not ok}
        if not failed:
            errors.append(f"неверное решение ничего не уронило: {mutant.name}")
        killed |= failed
    for name in sorted(set(first) - killed):
        errors.append(f"проверку не роняет ни одно неверное решение: {name}")
    return errors, len(first)


def check_docs(series, row):
    errors = []
    text = (series / "README.md").read_text(encoding="utf-8")
    headings = re.findall(r"^## (.+)$", text, re.M)
    if len(headings) != len(SECTIONS):
        errors.append(f"разделов {len(headings)}, а нужно {len(SECTIONS)}")
    for heading, pattern in zip(headings, SECTIONS):
        if pattern and not re.fullmatch(pattern, heading):
            errors.append(f"раздел «{heading}» вместо «{pattern}»")
    for name, low, high in (("README.md", 180, 300), ("theory.md", 110, 200)):
        count = len((series / name).read_text(encoding="utf-8").splitlines())
        if not low <= count <= high:
            errors.append(f"{name}: {count} строк вне {low}–{high}")
    header = text[:text.index("```", text.index("```") + 3)]
    for label, value in (("Концепт", row["concept"]), ("Артефакт", row["artifact"])):
        if f"{label}: {value}" not in header:
            errors.append(f"шапка: нет «{label}: {value}» из маршрута")
    if f"# {row['id']} — {row['title']}" not in text:
        errors.append("заголовок не совпадает с маршрутом")
    if "Навык разблокирован" not in text:
        errors.append("нет «Навык разблокирован»")
    return errors


def main():
    route = {row["id"]: row for row in read_series()}
    series_dirs = sorted(ROOT.glob("season-*/s[0-9][0-9]e[0-9][0-9]-*"))
    failed = 0
    for series in series_dirs:
        series_id = series.name[:6]
        errors, count = check_tests(series)
        errors += check_docs(series, route[series_id])
        print(f"{series_id}: {'проверок ' + str(count) if not errors else 'ЕСТЬ ОШИБКИ'}")
        for error in errors:
            print(f"  {error}")
        failed += bool(errors)
    print(f"Серии: {len(series_dirs)} проверено, с ошибками {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
