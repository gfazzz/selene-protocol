"""toolkit/cli.py — сводка и ответы одной командой. s01e12.

    python -m toolkit.cli summary ЖУРНАЛ [--low 96] [--high 104]
    python -m toolkit.cli answers ЖУРНАЛ [ЖУРНАЛ ...]

Готово: модули пакета и разбор журнала (`summary_lines`, `answer_lines`).
Твоя работа — `build_parser` и `main`. Сейчас `main` ничего не делает и
возвращает None, поэтому тест красный.

Договор `main(argv=None)`:
- argv — список аргументов без имени программы; None — взять sys.argv[1:];
- возвращает код возврата, а не завершает процесс: 0 — успех, 1 — журнал не
  найден или не читается, 2 — неверные аргументы;
- результат — в stdout, сообщения об ошибках — в stderr, и при ошибке stdout пуст.

`class` в `argparse` не нужен; `with` в `logfile` — приём записи (s02e09).
"""

import argparse
import sys

from .alerts import collect_alerts
from .errors import parse_all
from .logfile import read_log, selene_answers
from .presence import unknown_nodes

REGISTRY = set()
for number in range(1, 3001):
    REGISTRY.add(str(number).zfill(4))


def build_parser():
    """Парсер с двумя подкомандами:
    summary ЖУРНАЛ [--low 96] [--high 104] — числа с плавающей точкой;
    answers ЖУРНАЛ [ЖУРНАЛ ...] — хотя бы один журнал.
    """
    return None


def summary_lines(path, low, high):
    packets = []
    for line in read_log(path):
        if not line.startswith("#"):
            packets.append(line)
    accepted, rejected = parse_all(packets)
    pressure = []
    for reading in accepted:
        if reading[1] == "P":
            pressure.append(reading)
    alerts = collect_alerts(pressure, low, high)
    unknown = sorted(unknown_nodes(REGISTRY, accepted))
    return [
        f"журнал: {path}",
        f"принято: {len(accepted)}",
        f"отклонено: {len(rejected)}",
        f"тревог по давлению: {len(alerts)}",
        f"неизвестные узлы: {', '.join(unknown) if unknown else 'нет'}",
    ]


def answer_lines(paths):
    lines = []
    for path in paths:
        lines.append(f"== {path}")
        for note, answer in selene_answers(path):
            lines.append(f"{note} → {answer}")
    return lines


def main(argv=None):
    return None


if __name__ == "__main__":
    raise SystemExit(main())
