"""Неверное решение: count_runs_not_packets."""
"""toolkit/tally.py — сводка по узлам за смену. Эталон s01e04."""


def count_by_node(readings):
    counts = {}
    previous = None
    for reading in readings:
        node = reading[0]
        if node != previous:
            counts[node] = counts.get(node, 0) + 1
        previous = node
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
