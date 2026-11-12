"""Неверное решение: label_round_str."""
"""toolkit/labels.py — подписи для табло диспетчерской. Эталон s01e02."""


def normalize_code(code):
    return code.strip().upper()


def format_reading(node, sensor, value, sequence):
    return f"{node}  {normalize_code(sensor):<6}{str(round(value, 2)):>8}  #{sequence:06d}"


def join_codes(codes):
    return ", ".join(codes)


def field_note(name, raw):
    return f"поле {name}: {raw!r}"
