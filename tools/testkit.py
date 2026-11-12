"""Загрузка проверяемого кода (SPEC.md §3).

Обычный порядок: файл из `artifacts/`, а если его нет — эталон из `solution/`.
Переменная SELENE_SOURCE переопределяет его для проверок самого курса:
`solution`, `starter` или путь к файлу с заведомо неверным решением.

Неверное решение для многофайловой серии — один файл, первая строка которого
`# replaces: toolkit/__init__.py`: он подменяет этот файл в копии эталона.
"""

import atexit
import hashlib
import importlib.util
import os
import shutil
import tempfile
from pathlib import Path

_modules = {}
_sources = {}


def _forced():
    return os.environ.get("SELENE_SOURCE", "")


def _choose(series, relpath):
    forced = _forced()
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


def _overlay(solution_root, mutant):
    first = mutant.read_text(encoding="utf-8").splitlines()[0]
    if not first.startswith("# replaces: "):
        raise ValueError(f"{mutant}: первая строка должна быть '# replaces: <путь>'")
    target = first.removeprefix("# replaces: ").strip()
    root = Path(tempfile.mkdtemp(prefix="selene_"))
    atexit.register(shutil.rmtree, root, ignore_errors=True)
    shutil.copytree(solution_root, root, dirs_exist_ok=True)
    shutil.copyfile(mutant, root / target)
    return root


def package_root(test_file, package):
    """Каталог, который надо положить в sys.path, чтобы импортировать package."""
    series = Path(test_file).resolve().parents[1]
    forced = _forced()
    if forced == "solution":
        root, note = series / "solution", "эталон (задано SELENE_SOURCE)"
    elif forced == "starter":
        root, note = series / "starter", "каркас"
    elif forced:
        root, note = _overlay(series / "solution", Path(forced)), "задано SELENE_SOURCE"
    elif (series / "artifacts" / package / "__init__.py").exists():
        root, note = series / "artifacts", "твоё решение"
    else:
        root, note = series / "solution", f"artifacts/{package} нет — проверен эталон"
    _sources[series.name] = note
    return root


def source_report():
    return [f"{name}: {note}" for name, note in sorted(_sources.items())]
