"""Неверное решение: values_fromkeys_shared."""
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
        if node not in latest_number or sequence > latest_number[node]:
            latest_number[node] = sequence
            latest_value[node] = value
    return latest_value


def values_by_node(readings):
    nodes = []
    for reading in readings:
        nodes.append(reading[0])
    grouped = dict.fromkeys(nodes, [])
    for reading in readings:
        grouped[reading[0]].append(reading[2])
    return grouped
