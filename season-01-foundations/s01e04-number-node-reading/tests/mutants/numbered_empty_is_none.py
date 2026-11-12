"""Неверное решение: для пустого потока None вместо пустого списка."""
"""toolkit/walk.py — обход потока встроенными функциями. Эталон s01e04."""


def value_of(reading):
    return reading[2]


def worst(readings, n):
    ordered = sorted(readings, key=value_of, reverse=True)
    result = []
    for position, reading in enumerate(ordered):
        if position == n:
            break
        result.append(reading)
    return result


def numbered(readings, start=1):
    if not readings:
        return None
    return list(enumerate(readings, start))


def pair_up(nodes, values):
    return list(zip(nodes, values, strict=True))


def extremes(readings):
    if not readings:
        return None
    return min(readings, key=value_of), max(readings, key=value_of)
