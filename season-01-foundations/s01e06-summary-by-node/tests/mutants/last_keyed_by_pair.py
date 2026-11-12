"""Неверное решение: last_keyed_by_pair."""
"""toolkit/tally.py — сводка по узлам за смену. Эталон s01e06."""


def count_by_node(readings):
    counts = {}
    for reading in readings:
        node = reading[0]
        counts[node] = counts.get(node, 0) + 1
    return counts


def last_value_by_node(readings):
    latest_number = {}
    latest_value = {}
    for node, sensor, value, sequence, alarm in readings:
        key = (node, sensor)
        if key not in latest_number or sequence > latest_number[key]:
            latest_number[key] = sequence
            latest_value[key] = value
    return latest_value


def values_by_node(readings):
    grouped = {}
    for reading in readings:
        grouped.setdefault(reading[0], []).append(reading[2])
    return grouped
