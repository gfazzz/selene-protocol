"""Сводка смены: python -m toolkit <файл пакетов>.

Этот файл даёт курс. Он запускается только командой `python -m toolkit`,
а при `import toolkit` не выполняется. Чтение файла и `with` здесь — приём
записи: файлы разбираются в s01e08, `with` — в s02e05.
"""

import sys

from .alerts import collect_alerts, format_alert
from .reading import parse_reading
from .tally import count_by_node

LOW, HIGH = 96.0, 104.0  # давление в отсеке, кПа


def main(path):
    readings = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            if line.strip():
                readings.append(parse_reading(line))
    counts = count_by_node(readings)
    print(f"Сводка: пакетов {len(readings)}, узлов {len(counts)}")
    for node in sorted(counts):
        print(f"  {node}: {counts[node]}")
    for reading in collect_alerts(readings, LOW, HIGH):
        print(format_alert(reading))


if __name__ == "__main__":
    main(sys.argv[1])
