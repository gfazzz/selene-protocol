"""Неверное решение: unknown_all_reporting."""
"""toolkit/presence.py — кто докладывает, кто молчит, кто лишний. Эталон s01e07."""


def reporting_nodes(readings):
    nodes = set()
    for reading in readings:
        nodes.add(reading[0])
    return nodes


def silent_nodes(registry, readings):
    return registry - reporting_nodes(readings)


def unknown_nodes(registry, readings):
    return reporting_nodes(readings)
