"""Неверное решение: silent_discard_loop."""
"""toolkit/presence.py — кто докладывает, кто молчит, кто лишний. Эталон s01e07."""


def reporting_nodes(readings):
    nodes = set()
    for reading in readings:
        nodes.add(reading[0])
    return nodes


def silent_nodes(registry, readings):
    for node in reporting_nodes(readings):
        registry.discard(node)
    return registry


def unknown_nodes(registry, readings):
    return reporting_nodes(readings) - registry
