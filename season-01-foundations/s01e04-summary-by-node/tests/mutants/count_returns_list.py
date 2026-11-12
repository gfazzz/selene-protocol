"""Неверное решение: count_returns_list."""
"""toolkit/tally.py — сводка по узлам за смену. Эталон s01e04."""


def count_by_node(readings):
    nodes = []
    for reading in readings:
        nodes.append(reading[0])
    return nodes


def _reporting(readings):
    nodes = set()
    for reading in readings:
        nodes.add(reading[0])
    return nodes


def silent_nodes(registry, readings):
    return registry - _reporting(readings)


def unknown_nodes(registry, readings):
    return _reporting(readings) - registry
