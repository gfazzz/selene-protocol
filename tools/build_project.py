#!/usr/bin/env python3
"""Собирает сквозной проект сезона и прогоняет его проверку.

Сборка: эталоны всех серий сезона по порядку, поверх них — артефакты студента
(файл, указанный в docs/ROUTE.md, если он есть в artifacts/). Результат — в
season-NN-*/project/build/, проверка — season-NN-*/project/tests/.
"""

import os
import shutil
import subprocess
import sys

from route import ROOT, read_series


def build(season_dir):
    route = {row["id"]: row["artifact"].strip("`") for row in read_series()}
    build_dir = season_dir / "project" / "build"
    shutil.rmtree(build_dir, ignore_errors=True)
    build_dir.mkdir(parents=True)
    series_dirs = sorted(season_dir.glob("s[0-9][0-9]e[0-9][0-9]-*"))
    for series in series_dirs:
        shutil.copytree(series / "solution", build_dir, dirs_exist_ok=True)
    taken = []
    for series in series_dirs:
        relpath = route[series.name[:6]]
        artifact = series / "artifacts" / relpath
        if artifact.is_file():
            shutil.copyfile(artifact, build_dir / relpath)
            taken.append(f"{series.name[:6]}: {relpath}")
    return build_dir, taken


def main():
    season = os.environ.get("SEASON", "")
    seasons = sorted(ROOT.glob(f"season-{season}*-*" if season else "season-*"))
    failed = 0
    for season_dir in seasons:
        if not (season_dir / "project" / "tests").is_dir():
            continue
        build_dir, taken = build(season_dir)
        print(f"{season_dir.name}: собран проект, своих файлов {len(taken)}")
        for line in taken:
            print(f"  {line}")
        env = {**os.environ, "SELENE_PROJECT_ROOT": str(build_dir)}
        done = subprocess.run(
            [sys.executable, "-m", "pytest", str(season_dir / "project" / "tests"), "-q"],
            cwd=ROOT, env=env, check=False,
        )
        failed += done.returncode != 0
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
