"""Неверное решение: join_wrong_type."""
"""toolkit/labels.py — подписи для табло диспетчерской. Эталон s01e02."""


def normalize_code(code):
    return code.strip().upper()


def format_reading(node, sensor, value, sequence):
    return f"{node}  {normalize_code(sensor):<6}{value:>8.2f}  #{sequence:06d}"


def join_codes(codes):
    return str(codes)


def field_note(name, raw):
    return f"поле {name}: {raw!r}"
