"""Загрузка проверяемого модуля (SPEC.md §3).

Обычный порядок: файл из `artifacts/`, а если его нет — эталон из `solution/`.
Переменная SELENE_SOURCE переопределяет его для проверок самого курса:
`solution`, `starter` или путь к файлу с заведомо неверным решением.
"""

import hashlib
import importlib.util
import os
from pathlib import Path

_modules = {}
_sources = {}


def _choose(series, relpath):
    forced = os.environ.get("SELENE_SOURCE", "")
    artifact = series / "artifacts" / relpath
    solution = series / "solution" / relpath
    if forced == "solution":
        return solution, "эталон (задано SELENE_SOURCE)"
    if forced == "starter":
        single = series / "starter.py"
        return (single if single.exists() else series / "starter" / relpath), "каркас"
    if forced:
        return Path(forced).resolve(), "задано SELENE_SOURCE"
    if artifact.exists():
        return artifact, "твоё решение"
    return solution, f"artifacts/{relpath} нет — проверен эталон"


def load_artifact(test_file, relpath):
    """Загружает модуль серии, которой принадлежит test_file (она лежит в tests/)."""
    series = Path(test_file).resolve().parents[1]
    path, note = _choose(series, relpath)
    _sources[series.name] = note
    if path in _modules:
        return _modules[path]
    digest = hashlib.sha1(str(path).encode()).hexdigest()[:10]
    spec = importlib.util.spec_from_file_location(f"selene_{digest}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _modules[path] = module
    return module


def source_report():
    return [f"{name}: {note}" for name, note in sorted(_sources.items())]
