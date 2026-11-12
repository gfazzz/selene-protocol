"""Неверное решение: count_skips_first."""
"""toolkit/tally.py — сводка по узлам за смену. Эталон s01e04."""


def count_by_node(readings):
    counts = {}
    index = 1
    while index < len(readings):
        node = readings[index][0]
        counts[node] = counts.get(node, 0) + 1
        index += 1
    return counts


def _reporting(readings):
    nodes = set()
    for reading in readings:
        nodes.add(reading[0])
    return nodes


def silent_nodes(registry, readings):
    return registry - _reporting(readings)


def unknown_nodes(registry, readings):
    return _reporting(readings) - registry
