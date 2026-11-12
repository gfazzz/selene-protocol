"""Season 1 — приёмка сквозного проекта `toolkit`.

`make project SEASON=01` собирает пакет из твоих артефактов всех восьми серий
(нет артефакта — берётся эталон) и прогоняет здесь проверку на журнале смены из
s01e08. Каждая серия проверила свой модуль отдельно. Здесь проверяется, что они
работают вместе: что приняла одна функция, то сходится с тем, что посчитала
другая.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

SEASON = Path(__file__).resolve().parents[2]
LOG = SEASON / "s01e08-answer-in-the-log" / "data" / "shift_sol038.log"
REGISTRY = set()
for number in range(1, 3001):
    REGISTRY.add(str(number).zfill(4))
LOW, HIGH = 96.0, 104.0


@pytest.fixture(scope="module")
def root():
    value = os.environ.get("SELENE_PROJECT_ROOT")
    if not value:
        pytest.skip("Проект собирается командой make project SEASON=01")
    return Path(value)


@pytest.fixture(scope="module")
def tk(root):
    sys.path.insert(0, str(root))
    import toolkit
    from toolkit import errors, logfile

    toolkit.errors = errors
    toolkit.logfile = logfile
    return toolkit


@pytest.fixture(scope="module")
def shift(tk):
    lines = tk.logfile.read_log(LOG)
    packets = [line for line in lines if not line.startswith("#")]
    accepted, rejected = tk.errors.parse_all(packets)
    return lines, packets, accepted, rejected


def test_импорт_пакета_молчит_и_не_оставляет_файлов(root, tmp_path):
    done = subprocess.run(
        [sys.executable, "-c", "import toolkit"],
        cwd=tmp_path, env={**os.environ, "PYTHONPATH": str(root)},
        capture_output=True, text=True, check=False,
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout == "" and list(tmp_path.iterdir()) == [], (
        "Импорт toolkit печатает или создаёт файлы (s01e06)."
    )


def test_ни_одна_строка_журнала_не_потерялась(shift):
    lines, packets, accepted, rejected = shift
    assert packets, "В журнале не нашлось пакетов: проверь read_log (s01e08)."
    assert len(accepted) + len(rejected) == len(packets), (
        "Принято + отклонено должно равняться числу пакетов (s01e07)."
    )


def test_сводка_по_узлам_сходится_с_принятыми(tk, shift):
    accepted = shift[2]
    counts = tk.count_by_node(accepted)
    assert sum(counts.values()) == len(accepted), (
        "Сумма счётчиков по узлам не равна числу принятых пакетов (s01e04)."
    )


def test_узел_0000_неизвестен_справочнику(tk, shift):
    accepted = shift[2]
    unknown = tk.unknown_nodes(REGISTRY, accepted)
    silent = tk.silent_nodes(REGISTRY, accepted)
    assert "0000" in unknown, "Пакеты SELENE пришли с узла, которого нет в справочнике."
    assert not (unknown & REGISTRY) and silent <= REGISTRY


def test_тревоги_сходятся_между_модулями(tk, shift):
    accepted = shift[2]
    alerts = tk.collect_alerts(accepted, LOW, HIGH)
    counts = tk.count_alerts(accepted, LOW, HIGH)
    assert sum(counts.values()) == len(alerts), (
        "Тревог в списке и в счётчике по узлам разное количество (s01e05)."
    )
    values = [reading[2] for reading in accepted]
    breaches = tk.count_out_of_range(values, LOW, HIGH)
    first = tk.first_out_of_range(values, LOW, HIGH)
    assert (first is None) == (breaches == 0), (
        "first_out_of_range и count_out_of_range противоречат друг другу (s01e02)."
    )


def test_повторный_вызов_даёт_то_же(tk, shift):
    accepted = shift[2]
    first = tk.collect_alerts(accepted, LOW, HIGH)
    second = tk.collect_alerts(accepted, LOW, HIGH)
    assert first == second and first is not second, (
        "Второй вызов collect_alerts отличается от первого: состояние течёт (s01e05)."
    )


def test_ответы_selene_находятся_и_повторяются(tk, shift):
    accepted = shift[2]
    answers = tk.logfile.selene_answers(LOG)
    from_0000 = 0
    for reading in accepted:
        if reading[0] == "0000":
            from_0000 += 1
    assert answers, "В журнале смены есть ответы SELENE, а найдено ни одного (s01e08)."
    assert len(answers) <= from_0000
    assert tk.logfile.selene_answers(LOG) == answers


def test_сводка_из_командной_строки(root, tmp_path, shift):
    packets_file = tmp_path / "packets.txt"
    packets_file.write_text("\n".join(shift[1]) + "\n", encoding="utf-8")
    done = subprocess.run(
        [sys.executable, "-m", "toolkit", str(packets_file)],
        cwd=tmp_path, env={**os.environ, "PYTHONPATH": str(root)},
        capture_output=True, text=True, check=False,
    )
    assert done.returncode == 0 and done.stdout.strip(), (
        f"python -m toolkit завершился с кодом {done.returncode}: {done.stderr}"
    )
