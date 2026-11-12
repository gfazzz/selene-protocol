"""s01e08 — проверка `toolkit/logfile.py`.

Читать этот файл — законный ход: он и есть техническое задание. Главная проверка —
воспроизводимость находки: тест сам собирает журналы с разными seed, сажает в них
ответы и требует найти ровно посаженное. Ответ, вписанный в код руками, здесь не
проходит: в каждом журнале он свой.
"""

import importlib.util
import os
import random
import subprocess
import sys
from pathlib import Path

import pytest
from testkit import load_artifact

SERIES = Path(__file__).resolve().parents[1]
SEEDS = [7, 1969, 20261112]


@pytest.fixture(scope="module")
def logfile():
    return load_artifact(__file__, "toolkit/logfile.py")


def make_logs():
    spec = importlib.util.spec_from_file_location("s01e08_make_logs", SERIES / "tests" / "make_logs.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generated(seed):
    """Журнал со всеми трудными местами. Возвращает (строки, пары, байты файла)."""
    rng = random.Random(seed)
    lines, pairs = [], []
    for step in range(rng.randint(60, 90)):
        kind = rng.random()
        if kind < 0.12:
            note = f"{step // 60:02d}:{step % 60:02d} вопрос номер {step}, ёмкость {rng.randint(1, 9)}"
            lines.append("# " + note)
            follow = rng.random()
            if follow < 0.5:
                answer = rng.choice(["ДА", "НЕТ", "ПОЗЖЕ", "Я ЗДЕСЬ", "СПРОСИ ТАМУРУ"]) + f" {step}"
                lines.append(f"0000; {answer} ;0.00;{step};0")
                pairs.append((note, answer))
            elif follow < 0.7:
                # Обычный пакет между заметкой и пакетом 0000: это уже не ответ
                lines.append(f"{rng.randint(1, 3000):04d};O2;20.{step:02d};{step};0")
                lines.append(f"0000;НЕ ОТВЕТ {step};0.00;{step};0")
            else:
                # Заметка без ответа: за ней обычный пакет
                lines.append(f"{rng.randint(1, 3000):04d};T;21.{step:02d};{step};0")
        elif kind < 0.17:
            lines.append(f"0000;ПОТОК {step};0.00;{step};0")
        else:
            lines.append(f"{rng.randint(1, 3000):04d};P;{rng.uniform(96, 104):.2f};{step};0")
    # Две заметки подряд: у первой ответа нет
    lines.append("# 23:58 первая")
    lines.append("# 23:59 вторая")
    lines.append("0000;НА ВТОРУЮ;0.00;999;0")
    pairs.append(("23:59 вторая", "НА ВТОРУЮ"))
    newline = "\r\n" if seed % 2 else "\n"
    body = ""
    for line in lines:
        body += line + newline
        if rng.random() < 0.08:
            body += rng.choice(["", "   "]) + newline
    body = newline + body.removesuffix(newline)  # пустая в начале, последняя без перевода
    return lines, pairs, body.encode("utf-8")


def write(tmp_path, data, name="shift.log"):
    path = tmp_path / name
    path.write_bytes(data)
    return path


# read_log


@pytest.mark.parametrize("seed", SEEDS)
def test_журнал_читается_строка_в_строку(logfile, tmp_path, seed):
    lines, _, data = generated(seed)
    result = logfile.read_log(write(tmp_path, data))
    assert result == lines, (
        f"read_log вернула {len(result) if isinstance(result, list) else result!r} строк, "
        f"в журнале {len(lines)}. Пустые строки пропускаются, перевод строки в конце "
        "убирается, последняя строка без '\\n' остаётся."
    )


def test_последняя_строка_без_перевода_не_теряется(logfile, tmp_path):
    result = logfile.read_log(write(tmp_path, "# 01:00 раз\n0000;ДВА;0.00;2;0".encode()))
    assert result == ["# 01:00 раз", "0000;ДВА;0.00;2;0"], (
        f"Вернулось {result!r}. Последняя строка файла часто не кончается '\\n' — "
        "это всё ещё строка."
    )


def test_перевод_строки_не_остаётся_в_тексте(logfile, tmp_path):
    result = logfile.read_log(write(tmp_path, "# 01:00 раз\r\n# 01:01 два\n".encode()))
    assert result == ["# 01:00 раз", "# 01:01 два"], (
        f"Вернулось {result!r}. Символ конца строки — разметка файла, а не часть текста."
    )


def test_пустые_строки_пропускаются(logfile, tmp_path):
    result = logfile.read_log(write(tmp_path, "\n\n# 01:00 раз\n   \n\n# 01:01 два\n\n".encode()))
    assert result == ["# 01:00 раз", "# 01:01 два"], (
        f"Вернулось {result!r}. Пустые строки и строки из одних пробелов в счёт не идут."
    )


LOCALE_PROBE = "import sys; open(sys.argv[1]).read() == 'кто'.encode().decode('utf-8') or sys.exit(3)"
NON_UTF8 = {"LC_ALL": "C", "LANG": "C", "PYTHONCOERCECLOCALE": "0", "PYTHONUTF8": "0"}
READ_IN_SUBPROCESS = """
import importlib.util, sys
spec = importlib.util.spec_from_file_location("logfile", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(ascii(module.read_log(sys.argv[2])))
"""


def test_кодировка_задана_явно_а_не_взята_у_машины(logfile, tmp_path):
    probe = write(tmp_path, "кто".encode(), "probe.txt")
    env = {**os.environ, **NON_UTF8}
    check = subprocess.run([sys.executable, "-c", LOCALE_PROBE, str(probe)], env=env,
                           capture_output=True, check=False)
    if check.returncode == 0:
        pytest.skip("на этой машине не удалось включить кодировку по умолчанию, отличную от UTF-8")
    path = write(tmp_path, "# 02:01 кто это?\n0000;ВСЁ ЕЩЁ Я;0.00;1;0\n".encode())
    done = subprocess.run([sys.executable, "-c", READ_IN_SUBPROCESS, logfile.__file__, str(path)],
                          env=env, capture_output=True, text=True, check=False)
    expected = ascii(["# 02:01 кто это?", "0000;ВСЁ ЕЩЁ Я;0.00;1;0"])
    assert done.returncode == 0 and done.stdout.strip() == expected, (
        "На машине, где кодировка по умолчанию не UTF-8, журнал не прочитался "
        f"(код {done.returncode}, {done.stderr.strip().splitlines()[-1:] or done.stdout.strip()}). "
        "open() без encoding берёт кодировку у системы. Укажи encoding='utf-8'."
    )


# selene_answer


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("0000;ТА, КТО ОТВЕЧАЕТ;0.00;485;0", "ТА, КТО ОТВЕЧАЕТ"),
        ("0000;  Я ЗДЕСЬ ;0.00;1;0", "Я ЗДЕСЬ"),
        ("0214;O2;20.90;118;0", None),
        ("# 03:55 0000;ПОДДЕЛКА;0.00;1;0", None),
    ],
)
def test_ответ_это_поле_датчика_пакета_0000(logfile, line, expected):
    result = logfile.selene_answer(line)
    assert result == expected, (
        f"selene_answer({line!r}) вернула {result!r}, а ждём {expected!r}. Ответ — поле "
        "датчика пакета с узла 0000, без пробелов по краям; заметка ответом не бывает."
    )


# selene_answers


@pytest.mark.parametrize("seed", SEEDS)
def test_находит_ровно_посаженные_ответы(logfile, tmp_path, seed):
    _, pairs, data = generated(seed)
    result = logfile.selene_answers(write(tmp_path, data))
    assert result == pairs, (
        f"Найдено {result!r}, а посажено {pairs!r}. Ответ — только пакет 0000 сразу после "
        "заметки; заметка возвращается без '# ' и без перевода строки."
    )


def test_повторный_прогон_даёт_то_же(logfile, tmp_path):
    _, pairs, data = generated(SEEDS[0])
    path = write(tmp_path, data)
    first, second = logfile.selene_answers(path), logfile.selene_answers(path)
    assert first == second == pairs, "Два прогона по одному журналу должны давать одну находку."


@pytest.mark.parametrize(("name", "build"), [("shift_rejes.log", "rejes_log"), ("shift_sol038.log", "sol038_log")])
def test_находка_в_журналах_серии(logfile, name, build):
    _, planted = getattr(make_logs(), build)()
    result = logfile.selene_answers(SERIES / "data" / name)
    assert result == planted, f"В data/{name} найдено {result!r}, а там {planted!r}."


def test_последний_ответ_рейесу(logfile):
    result = logfile.selene_answers(SERIES / "data" / "shift_rejes.log")
    assert result and result[len(result) - 1] == ("03:55 ты кто вообще такая", "ТА, КТО ОТВЕЧАЕТ"), (
        f"Последняя пара в журнале Рейеса: {result[len(result) - 1] if result else result!r}."
    )
