"""Неверное решение: join_trailing_separator."""
"""toolkit/labels.py — подписи для табло диспетчерской. Эталон s01e02."""


def normalize_code(code):
    return code.strip().upper()


def format_reading(node, sensor, value, sequence):
    return f"{node}  {normalize_code(sensor):<6}{value:>8.2f}  #{sequence:06d}"


def join_codes(codes):
    result = ""
    for code in codes:
        result = result + code + ", "
    return result


def field_note(name, raw):
    return f"поле {name}: {raw!r}"
