"""Неверное решение: count_keys_int."""
"""toolkit/tally.py — сводка по узлам за смену. Эталон s01e04."""


def count_by_node(readings):
    counts = {}
    for reading in readings:
        node = int(reading[0])
        counts[node] = counts.get(node, 0) + 1
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
