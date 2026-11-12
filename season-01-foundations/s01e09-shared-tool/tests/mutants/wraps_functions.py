# replaces: toolkit/__init__.py
"""toolkit — библиотека колонии. Эталон s01e09."""

from .alerts import collect_alerts, count_alerts, format_alert
from .labels import field_note, format_reading, join_codes, normalize_code
from .presence import reporting_nodes, silent_nodes, unknown_nodes
from .reading import (
    parse_reading,
    read_alarm,
    read_node,
    read_sensor,
    read_sequence,
    read_value,
)
from .scan import count_out_of_range, first_gap, first_out_of_range
from .tally import count_by_node, last_value_by_node, values_by_node
from .walk import extremes, numbered, pair_up, worst
from .window import board, moving_windows, snapshot

__version__ = "0.1.0"

from . import alerts, labels, presence, tally, walk, window


def format_reading(node, sensor, value, sequence):
    """Обёртка «для удобства»."""
    return labels.format_reading(node, sensor, value, sequence)


def count_by_node(readings):
    return tally.count_by_node(readings)


def worst(readings, n):
    return walk.worst(readings, n)


def board(rows, cols, fill):
    """Обёртка «для удобства»."""
    return window.board(rows, cols, fill)


def silent_nodes(registry, readings):
    return presence.silent_nodes(registry, readings)


def format_alert(reading, prefix="ТРЕВОГА"):
    return alerts.format_alert(reading, prefix)

__all__ = [
    "read_node", "read_sensor", "read_value", "read_sequence", "read_alarm",
    "parse_reading",
    "normalize_code", "format_reading", "join_codes", "field_note",
    "first_out_of_range", "count_out_of_range", "first_gap",
    "worst", "numbered", "pair_up", "extremes",
    "moving_windows", "board", "snapshot",
    "count_by_node", "last_value_by_node", "values_by_node",
    "reporting_nodes", "silent_nodes", "unknown_nodes",
    "collect_alerts", "format_alert", "count_alerts",
]
