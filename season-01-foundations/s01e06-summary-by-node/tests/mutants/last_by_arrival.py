"""Неверное решение: last_by_arrival."""
"""toolkit/tally.py — сводка по узлам за смену. Эталон s01e06."""


def count_by_node(readings):
    counts = {}
    for reading in readings:
        node = reading[0]
        counts[node] = counts.get(node, 0) + 1
    return counts


def last_value_by_node(readings):
    latest_value = {}
    for node, sensor, value, sequence, alarm in readings:
        latest_value[node] = value
    return latest_value


def values_by_node(readings):
    grouped = {}
    for reading in readings:
        grouped.setdefault(reading[0], []).append(reading[2])
    return grouped
