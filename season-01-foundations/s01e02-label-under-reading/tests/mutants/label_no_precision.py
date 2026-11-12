"""Неверное решение: label_no_precision."""
"""toolkit/labels.py — подписи для табло диспетчерской. Эталон s01e02."""


def normalize_code(code):
    return code.strip().upper()


def format_reading(node, sensor, value, sequence):
    return f"{node}  {normalize_code(sensor):<6}{value:>8}  #{sequence:06d}"


def join_codes(codes):
    return ", ".join(codes)


def field_note(name, raw):
    return f"поле {name}: {raw!r}"
