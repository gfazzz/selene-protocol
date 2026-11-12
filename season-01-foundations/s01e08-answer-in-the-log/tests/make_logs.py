#!/usr/bin/env python3
"""Собирает журналы смен серии s01e08 из фиксированного seed.

    python3 tests/make_logs.py      # перезаписывает data/*.log

Тест серии зовёт те же функции и сверяет найденное с посаженным: если журнал
поменяется, ожидание поменяется вместе с ним.
"""

import random
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"

SENSORS = {"O2": (19.5, 23.5), "P": (96.0, 104.0), "CO2": (0.03, 0.45), "T": (18.0, 26.0)}

# (минута смены, заметка, ответ SELENE или None)
REJES_NOTES = [
    (5, "00:05 принял смену", None),
    (41, "00:41 опять 0000 в потоке", None),
    (78, "01:18 узел 0000 — это кто?", "НЕ УЗЕЛ"),
    (102, "01:42 давление 1187 в норме", None),
    (131, "02:11 проверка связи", "СВЯЗЬ ЕСТЬ. ПРОВЕРКИ НЕТ"),
    (160, "02:40 тамура говорит, это эхо ретранслятора", "ТАМУРА ОШИБАЕТСЯ ВЕЖЛИВО"),
    (188, "03:08 завтра пишу в службу связи", None),
    (213, "03:33 если ты эхо, повтори", "ЕСЛИ ТЫ ЭХО, ПОВТОРИ"),
    (235, "03:55 ты кто вообще такая", "ТА, КТО ОТВЕЧАЕТ"),
    (262, "04:22 сдал смену", None),
]

SOL038_NOTES = [
    (8, "00:08 прогоняю архив журналов", None),
    (47, "00:47 ты отвечала Рейесу?", "ОН СПРАШИВАЛ"),
    (80, "01:20 и он улетел", None),
    (116, "01:56 почему он, а потом я", "ВЫ ОБА ЧИТАЕТЕ ПОТОК"),
    (121, "02:01 кто это?", "ВСЁ ЕЩЁ Я"),
]


def packet(rng, node, sequence):
    sensor = rng.choice(sorted(SENSORS))
    low, high = SENSORS[sensor]
    value = rng.uniform(low, high)
    alarm = "1" if rng.random() < 0.01 else "0"
    return f"{node};{sensor};{value:.2f};{sequence};{alarm}"


def build(seed, notes, minutes=270, per_minute=2):
    """Текст журнала и посаженные пары (заметка, ответ) в порядке появления."""
    rng = random.Random(seed)
    lines, planted, sequence = [], [], 1
    by_minute = {minute: (note, answer) for minute, note, answer in notes}
    for minute in range(minutes):
        for _ in range(per_minute):
            lines.append(packet(rng, f"{rng.randint(1, 3000):04d}", sequence))
            sequence += 1
            # Пакеты SELENE, которые ни на что не отвечают
            if rng.random() < 0.02:
                lines.append(f"0000;ПОТОК ИДЁТ;0.00;{sequence};0")
                sequence += 1
        if minute in by_minute:
            note, answer = by_minute[minute]
            lines.append(f"# {note}")
            if answer is not None:
                lines.append(f"0000;{answer};0.00;{sequence};0")
                sequence += 1
                planted.append((note, answer))
    return "\n".join(lines) + "\n", planted


def rejes_log():
    return build(20260225, REJES_NOTES)


def sol038_log():
    return build(20261108, SOL038_NOTES, minutes=130)


def main():
    for name, (text, _) in (("shift_rejes.log", rejes_log()), ("shift_sol038.log", sol038_log())):
        (DATA / name).write_text(text, encoding="utf-8")
        print(f"data/{name}: {text.count(chr(10))} строк")


if __name__ == "__main__":
    main()
