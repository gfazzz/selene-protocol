"""Неверное решение: как у Рейеса: при равных значениях решает код узла."""
"""toolkit/walk.py — обход потока встроенными функциями. Эталон s01e04."""


def value_of(reading):
    return reading[2]


def worst(readings, n):
    def value_and_node(reading):
        return reading[2], reading[0]
    ordered = sorted(readings, key=value_and_node, reverse=True)
    result = []
    for position, reading in enumerate(ordered):
        if position == n:
            break
        result.append(reading)
    return result


def numbered(readings, start=1):
    return list(enumerate(readings, start))


def pair_up(nodes, values):
    return list(zip(nodes, values, strict=True))


def extremes(readings):
    if not readings:
        return None
    return min(readings, key=value_of), max(readings, key=value_of)
