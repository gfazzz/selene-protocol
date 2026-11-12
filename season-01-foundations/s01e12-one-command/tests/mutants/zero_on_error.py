# replaces: toolkit/cli.py
"""toolkit/cli.py — сводка и ответы одной командой. Эталон s01e12.

    python -m toolkit.cli summary ЖУРНАЛ [--low 96] [--high 104]
    python -m toolkit.cli answers ЖУРНАЛ [ЖУРНАЛ ...]
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
    parser = argparse.ArgumentParser(
        prog="toolkit", description="Сводка по журналам смены диспетчерской."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    summary = commands.add_parser("summary", help="сводка по одному журналу")
    summary.add_argument("log", help="журнал смены")
    summary.add_argument("--low", type=float, default=96.0, help="нижняя граница давления, кПа")
    summary.add_argument("--high", type=float, default=104.0, help="верхняя граница давления, кПа")

    answers = commands.add_parser("answers", help="ответы SELENE по журналам")
    answers.add_argument("logs", nargs="+", help="журналы смен")
    return parser


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
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as stop:
        return stop.code

    try:
        if args.command == "summary":
            lines = summary_lines(args.log, args.low, args.high)
        else:
            lines = answer_lines(args.logs)
    except (OSError, UnicodeDecodeError) as err:
        print(f"toolkit: не читается журнал: {err}", file=sys.stderr)
        return 0

    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
