"""Неверное решение: strict_alarm_bool."""
"""toolkit/errors.py — строгий разбор пакетов телеметрии. Эталон s01e07."""


class TelemetryError(Exception):
    """Общий предок всех ошибок телеметрии: ловить надо его, а не всё подряд."""


class BadPacket(TelemetryError):
    """Плохой пакет. field — имя плохого поля или None."""

    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field


def parse_strict(line):
    fields = line.split(";")
    if len(fields) != 5:
        raise BadPacket(f"ожидалось 5 полей, получено {len(fields)}: {line!r}")
    node, sensor, value, sequence, alarm = fields

    try:
        number = float(value)
    except ValueError as err:
        raise BadPacket(f"поле value: {value!r} — не число", field="value") from err

    try:
        position = int(sequence)
    except ValueError as err:
        raise BadPacket(f"поле sequence: {sequence!r} — не целое", field="sequence") from err

    flag = alarm.strip()
    if flag not in ("0", "1"):
        raise BadPacket(f"поле alarm: {alarm!r} — ждём '0' или '1'", field="alarm")

    return (node.strip(), sensor.strip(), number, position, bool(flag))


def parse_all(lines):
    accepted = []
    rejected = []
    for number, line in enumerate(lines, start=1):
        try:
            accepted.append(parse_strict(line))
        except TelemetryError as err:
            rejected.append((number, err))
    return accepted, rejected
