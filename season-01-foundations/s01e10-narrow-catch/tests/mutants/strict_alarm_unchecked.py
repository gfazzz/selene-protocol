"""Неверное решение: strict_alarm_unchecked."""
"""toolkit/errors.py — строгий разбор пакетов телеметрии. Эталон s01e10."""


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

    return (node.strip(), sensor.strip(), number, position, flag == "1")


def parse_all(lines):
    accepted = []
    rejected = []
    for number, line in enumerate(lines, start=1):
        try:
            accepted.append(parse_strict(line))
        except TelemetryError as err:
            rejected.append((number, err))
    return accepted, rejected
