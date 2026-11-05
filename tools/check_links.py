#!/usr/bin/env python3
"""Ищет битые относительные ссылки в .md (без якорей и внешних адресов)."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".venv", ".git", "build"}
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def main():
    broken = 0
    for path in ROOT.rglob("*.md"):
        parts = set(path.relative_to(ROOT).parts)
        if parts & SKIP or any(p.startswith("_backup-") for p in parts):
            continue
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("mailto:"):
                continue
            if not (path.parent / target).exists():
                print(f"битая ссылка: {path.relative_to(ROOT)} → {target}")
                broken += 1
    print("Ссылки: всё на месте" if not broken else f"Ссылки: битых {broken}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
