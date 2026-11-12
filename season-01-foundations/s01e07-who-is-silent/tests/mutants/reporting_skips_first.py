"""Неверное решение: reporting_skips_first."""
"""toolkit/presence.py — кто докладывает, кто молчит, кто лишний. Эталон s01e07."""


def reporting_nodes(readings):
    nodes = set()
    index = 1
    while index < len(readings):
        nodes.add(readings[index][0])
        index += 1
    return nodes


def silent_nodes(registry, readings):
    return registry - reporting_nodes(readings)


def unknown_nodes(registry, readings):
    return reporting_nodes(readings) - registry
