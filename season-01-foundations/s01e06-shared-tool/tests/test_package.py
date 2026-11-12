"""s01e06 — проверка пакета `toolkit`.

Читать этот файл — законный ход: он и есть техническое задание. Каждая проверка
запускает отдельный процесс Python в пустом временном каталоге: так видно, что
импорт напечатал и какие файлы после себя оставил.
"""

import json
import os
import subprocess
import sys

import pytest
from testkit import package_root

PUBLIC = {
    "reading": ["read_node", "read_sensor", "read_value", "read_sequence",
                "read_alarm", "parse_reading"],
    "scan": ["first_out_of_range", "count_out_of_range", "first_gap"],
    "window": ["moving_windows", "board", "snapshot"],
    "tally": ["count_by_node", "silent_nodes", "unknown_nodes"],
    "alerts": ["collect_alerts", "format_alert", "count_alerts"],
}
EXPECTED = {name for names in PUBLIC.values() for name in names}


@pytest.fixture(scope="module")
def root():
    return package_root(__file__, "toolkit")


def run(root, cwd, *args):
    env = {**os.environ, "PYTHONPATH": str(root)}
    return subprocess.run(
        [sys.executable, *args], cwd=cwd, env=env,
        capture_output=True, text=True, timeout=30, check=False,
    )


def python(root, cwd, code):
    done = run(root, cwd, "-c", code)
    assert done.returncode == 0, f"Код упал:\n{code}\n{done.stderr}"
    return done


def last_json(done):
    """Ответ проверки — последняя строка вывода; всё, что выше, напечатал пакет."""
    return json.loads(done.stdout.splitlines()[-1])


# Импорт без побочных эффектов


def test_импорт_ничего_не_печатает(root, tmp_path):
    done = python(root, tmp_path, "import toolkit")
    assert done.stdout == "" and done.stderr == "", (
        f"import toolkit напечатал:\n{done.stdout}{done.stderr}\n"
        "Импорт — это вопрос «дай мне функции». Отвечать на него баннером не надо."
    )


def test_импорт_не_создаёт_файлов(root, tmp_path):
    python(root, tmp_path, "import toolkit")
    left = sorted(path.name for path in tmp_path.iterdir())
    assert left == [], (
        f"После import toolkit в текущем каталоге появились файлы: {left}. "
        "Импорт выполняется в каталоге того, кто импортирует, — не твоём."
    )


# Что пакет обещает


def names(root, tmp_path, expression):
    done = python(root, tmp_path, f"import json, toolkit\nprint(json.dumps({expression}))")
    return last_json(done)


def test_версия_объявлена(root, tmp_path):
    version = names(root, tmp_path, "getattr(toolkit, '__version__', None)")
    assert version == "0.1.0", (
        f"toolkit.__version__ = {version!r}. Ждём строку '0.1.0': версию читают "
        "люди и программы, и сравнивать её как число нельзя — 0.10 не больше 0.9."
    )


def test_all_перечисляет_ровно_публичные_функции(root, tmp_path):
    declared = names(root, tmp_path, "getattr(toolkit, '__all__', None)")
    assert declared is not None, "В пакете нет __all__: непонятно, что он обещает."
    assert len(declared) == len(set(declared)), f"В __all__ есть повторы: {declared}"
    extra = sorted(set(declared) - EXPECTED)
    missing = sorted(EXPECTED - set(declared))
    assert not extra and not missing, (
        f"Лишнее в __all__: {extra}. Не хватает: {missing}. Наружу выходят функции "
        "модулей, а не сами модули и не служебные имена."
    )


def test_звёздочка_даёт_ровно_all(root, tmp_path):
    code = (
        "import json, toolkit\n"
        "space = {}\n"
        "exec('from toolkit import *', space)\n"
        "got = sorted(name for name in space if not name.startswith('_'))\n"
        "print(json.dumps([got, sorted(getattr(toolkit, '__all__', []))]))"
    )
    done = run(root, tmp_path, "-c", code)
    assert done.returncode == 0, (
        f"from toolkit import * упал:\n{done.stderr}\nКаждое имя из __all__ должно "
        "существовать в пакете."
    )
    got, declared = last_json(done)
    assert got == declared, (
        f"from toolkit import * дал {got}, а __all__ обещает {declared}."
    )


@pytest.mark.parametrize("module", sorted(PUBLIC))
def test_имя_пакета_это_функция_модуля(root, tmp_path, module):
    code = (
        "import json, toolkit\n"
        f"import toolkit.{module} as module\n"
        f"wrong = [name for name in {PUBLIC[module]!r}\n"
        "         if getattr(toolkit, name, None) is not getattr(module, name)]\n"
        "print(json.dumps(wrong))"
    )
    wrong = last_json(python(root, tmp_path, code))
    assert wrong == [], (
        f"toolkit.{wrong[0] if wrong else ''} — не тот объект, что в toolkit.{module}. "
        "Пакет отдаёт функции модулей, а не копии и не обёртки: иначе исправление в "
        "модуле не дойдёт до тех, кто импортирует пакет."
    )


def test_функции_пакета_работают(root, tmp_path):
    code = (
        "import json, toolkit\n"
        "print(json.dumps([toolkit.parse_reading('0214;P;101.30;401;0'),\n"
        "                  toolkit.first_gap([5, 6, 8]),\n"
        "                  toolkit.first_out_of_range([100.0, 95.0], 96.0, 104.0)]))"
    )
    got = last_json(python(root, tmp_path, code))
    assert got == [["0214", "P", 101.3, 401, False], 7, 1], (
        f"Функции пакета вернули {got}. Похоже, под одним именем лежит другая функция."
    )


# Запуск пакета как программы


def test_python_m_toolkit_печатает_сводку_и_только_её(root, tmp_path):
    packets = tmp_path / "packets.txt"
    packets.write_text("0214;P;101.30;401;0\n2210;P;95.40;402;0\n", encoding="utf-8")
    done = run(root, tmp_path, "-m", "toolkit", "packets.txt")
    assert done.returncode == 0, f"python -m toolkit упал:\n{done.stderr}"
    lines = done.stdout.splitlines()
    assert lines and lines[0] == "Сводка: пакетов 2, узлов 2", (
        f"Первая строка вывода: {lines[:1]}. Сводка должна начинаться сразу, без баннера."
    )
    assert "ТРЕВОГА 2210 P 95.4 #402" in lines
    left = sorted(path.name for path in tmp_path.iterdir())
    assert left == ["packets.txt"], f"После запуска остались лишние файлы: {left}"
