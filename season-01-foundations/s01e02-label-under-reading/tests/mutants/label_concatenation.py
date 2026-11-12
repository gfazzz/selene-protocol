"""Неверное решение: label_concatenation."""
"""toolkit/labels.py — подписи для табло диспетчерской. Эталон s01e02."""


def normalize_code(code):
    return code.strip().upper()


def format_reading(node, sensor, value, sequence):
    return node + "  " + normalize_code(sensor) + " " + str(value) + "  #" + str(sequence)


def join_codes(codes):
    return ", ".join(codes)


def field_note(name, raw):
    return f"поле {name}: {raw!r}"
