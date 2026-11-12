"""s01e12 — проверка `toolkit/cli.py`.

Читать этот файл — законный ход: он и есть техническое задание. Программу
проверяют двумя способами: вызовом `main(argv)` в этом же процессе (видно код
возврата, stdout и stderr по отдельности) и настоящим запуском
`python -m toolkit.cli` в отдельном процессе — так её запустит Окафор.
"""

import importlib
import os
import subprocess
import sys
from pathlib import Path

import pytest
from testkit import package_root

SEASON = Path(__file__).resolve().parents[2]
DATA = SEASON / "s01e11-answer-in-the-log" / "data"
REJES_FIRST = DATA / "shift_rejes_first.log"
REJES = DATA / "shift_rejes.log"
SOL038 = DATA / "shift_sol038.log"

# Журнал, где ответ известен заранее: 6 пакетов, из них 2 битых; давление
# в узле 0042 вне 96–104 дважды; у 0007 поднят флаг; узел 0000 вне справочника.
SHIFT = """\
# 21:00 начало смены
0042;P;95.10;1;0
0042;P;99.00;2;0
0007;P;100.00;3;1
0042;P;104.90;4;0
0042;P;9,6;5;0
0000;КТО ЗДЕСЬ;0.00;6;0
0311;T;обрыв;7;0
"""


@pytest.fixture(scope="module")
def root():
    return package_root(__file__, "toolkit")


@pytest.fixture(scope="module")
def cli(root):
    for name in list(sys.modules):
        if name == "toolkit" or name.startswith("toolkit."):
            del sys.modules[name]
    sys.path.insert(0, str(root))
    try:
        module = importlib.import_module("toolkit.cli")
    finally:
        sys.path.remove(str(root))
    yield module
    for name in list(sys.modules):
        if name == "toolkit" or name.startswith("toolkit."):
            del sys.modules[name]


@pytest.fixture
def shift(tmp_path):
    path = tmp_path / "shift.log"
    path.write_text(SHIFT, encoding="utf-8")
    return path


def call(cli, capsys, *argv):
    code = cli.main(list(argv))
    out, err = capsys.readouterr()
    return code, out, err


def run(root, *argv, cwd=None):
    env = {**os.environ, "PYTHONPATH": str(root)}
    return subprocess.run(
        [sys.executable, "-m", "toolkit.cli", *argv], cwd=cwd, env=env,
        capture_output=True, text=True, timeout=30, check=False,
    )


def field(out, name):
    for line in out.splitlines():
        if line.startswith(name + ":"):
            return line.removeprefix(name + ":").strip()
    pytest.fail(f"В выводе нет строки «{name}: …». Вывод:\n{out}")


# Успех: код 0, результат в stdout


def test_main_возвращает_код_а_не_завершает_процесс(cli, capsys, shift):
    try:
        code = cli.main(["summary", str(shift)])
    except SystemExit as stop:
        pytest.fail(
            f"main поднял SystemExit({stop.code!r}). Код возврата main возвращает "
            "через return, а завершает процесс одна строка внизу модуля."
        )
    capsys.readouterr()
    assert type(code) is int and code == 0, (
        f"main(['summary', ...]) вернул {code!r}. Успех — это целое 0."
    )


def test_сводка_считает_принятые_отклонённые_и_тревоги(cli, capsys, shift):
    code, out, err = call(cli, capsys, "summary", str(shift))
    assert code == 0 and err == "", f"Код {code}, stderr:\n{err}"
    assert field(out, "принято") == "5"
    assert field(out, "отклонено") == "2"
    assert field(out, "тревог по давлению") == "3", (
        "Тревоги давления в этом журнале: 95.1 и 104.9 вне 96–104, и флаг у 0007."
    )
    assert field(out, "неизвестные узлы") == "0000"


def test_границы_берутся_из_аргументов(cli, capsys, shift):
    code, out, _ = call(cli, capsys, "summary", str(shift), "--low", "90", "--high", "110")
    assert code == 0
    assert field(out, "тревог по давлению") == "1", (
        "С --low 90 --high 110 вне границ нет ни одного давления, остаётся только флаг 0007. "
        "Если тревог по-прежнему три — аргументы разобраны, но не дошли до расчёта."
    )
    code, out, _ = call(cli, capsys, "summary", str(shift), "--low", "99.5")
    assert code == 0 and field(out, "тревог по давлению") == "4"


def test_ответы_по_журналу_рейеса(cli, capsys):
    code, out, err = call(cli, capsys, "answers", str(REJES))
    assert code == 0 and err == "", f"Код {code}, stderr:\n{err}"
    assert "03:55 ты кто вообще такая → ТА, КТО ОТВЕЧАЕТ" in out.splitlines(), (
        "В выводе нет последней пары Рейеса в виде «заметка → ответ»."
    )


def test_ответы_по_всем_журналам_сразу(cli, capsys):
    code, out, _ = call(cli, capsys, "answers", str(REJES), str(SOL038))
    assert code == 0
    headers = [line for line in out.splitlines() if line.startswith("== ")]
    assert headers == [f"== {REJES}", f"== {SOL038}"], (
        f"Заголовки журналов в выводе: {headers!r}. Каждый переданный журнал — "
        "своим заголовком, в том порядке, в каком переданы."
    )


def test_одной_командой_по_всем_журналам_рейеса(cli, capsys):
    code, out, err = call(cli, capsys, "answers", str(REJES_FIRST), str(REJES))
    first = out.find("ТА, КТО СПРАШИВАЕТ В ОТВЕТ")
    last = out.find("ТА, КТО ОТВЕЧАЕТ")
    assert code == 0 and err == "", f"Код {code}, stderr: {err!r}."
    assert 0 <= first < last, (
        "Одна команда по первому и последнему журналу Рейеса должна найти оба ответа, "
        "и в порядке журналов: сначала «ТА, КТО СПРАШИВАЕТ В ОТВЕТ», потом «ТА, КТО ОТВЕЧАЕТ»."
    )


def test_справка_в_stdout_с_кодом_0(cli, capsys):
    code, out, _ = call(cli, capsys, "--help")
    assert code == 0 and "summary" in out and "answers" in out, (
        f"--help вернул {code!r}. Справка — это успешный ответ: код 0, текст в stdout."
    )


def test_без_argv_читает_sys_argv(cli, capsys, shift, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["toolkit", "summary", str(shift)])
    code = cli.main()
    out, _ = capsys.readouterr()
    assert code == 0 and field(out, "принято") == "5", (
        "main() без аргументов должен взять sys.argv[1:]."
    )


# Отказ: код 1 или 2, сообщение в stderr, stdout пуст


def test_нет_файла_это_код_1(cli, capsys, tmp_path):
    missing = tmp_path / "нет-такого.log"
    try:
        code, out, err = call(cli, capsys, "summary", str(missing))
    except OSError as error:
        pytest.fail(
            f"main упал с {type(error).__name__}. Отсутствующий журнал — обычная "
            "ситуация для программы: код 1 и одна понятная строка в stderr."
        )
    assert code == 1, f"Нет файла, а main вернул {code!r}. Ждём 1."
    assert out == "", f"При ошибке в stdout ушло:\n{out}\nОшибка — в stderr."
    assert "нет-такого.log" in err, f"В stderr не назван файл: {err!r}"


def test_один_плохой_журнал_из_нескольких(cli, capsys, tmp_path):
    missing = tmp_path / "пропал.log"
    code, out, err = call(cli, capsys, "answers", str(REJES), str(missing))
    assert code == 1 and "пропал.log" in err
    assert out == "", (
        "Второй журнал не прочитался, а в stdout уже ушли ответы первого. Тот, кто "
        "передаст вывод дальше, примет неполный результат за полный."
    )


@pytest.mark.parametrize(
    "argv",
    [["frobnicate"], [], ["summary"], ["summary", "x.log", "--low", "abc"], ["answers"]],
)
def test_неверные_аргументы_это_код_2(cli, capsys, argv):
    try:
        code, out, err = call(cli, capsys, *argv)
    except SystemExit as stop:
        pytest.fail(
            f"main({argv!r}) поднял SystemExit({stop.code!r}): так argparse сообщает "
            "о неверных аргументах. Перехвати его и верни код из main."
        )
    assert code == 2, f"main({argv!r}) вернул {code!r}. Неверные аргументы — код 2."
    assert out == "" and "usage" in err, (
        f"stdout: {out!r}\nstderr: {err!r}\nПодсказка по вызову — в stderr, stdout пуст."
    )


# Настоящий запуск


def test_запуск_командой_даёт_тот_же_вывод(cli, capsys, root, shift):
    _, expected, _ = call(cli, capsys, "summary", str(shift))
    done = run(root, "summary", str(shift))
    assert done.returncode == 0 and done.stdout == expected, (
        f"python -m toolkit.cli: код {done.returncode}\n{done.stdout}{done.stderr}"
    )


def test_запуск_без_файла_без_трассировки(root, tmp_path):
    done = run(root, "summary", str(tmp_path / "нет.log"))
    assert done.returncode == 1 and done.stdout == "", (
        f"Код {done.returncode}, stdout {done.stdout!r}."
    )
    assert "Traceback" not in done.stderr, (
        "Вместо одной строки в stderr — трассировка. Код 1 у неё случайный: так "
        "Python завершается при любом непойманном исключении."
    )


def test_запуск_с_неверным_аргументом(root):
    done = run(root, "frobnicate")
    assert done.returncode == 2 and done.stdout == "" and "usage" in done.stderr


def test_импорт_модуля_ничего_не_запускает(root, tmp_path):
    env = {**os.environ, "PYTHONPATH": str(root)}
    done = subprocess.run(
        [sys.executable, "-c", "import toolkit.cli"], cwd=tmp_path, env=env,
        capture_output=True, text=True, timeout=30, check=False,
    )
    assert done.returncode == 0 and done.stdout == "" and done.stderr == "", (
        "import toolkit.cli что-то напечатал или упал: main вызван при импорте. "
        "Запуск — только под if __name__ == '__main__'."
    )
