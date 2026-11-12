# replaces: toolkit/__init__.py
"""toolkit — библиотека колонии. Эталон s01e06."""

from .alerts import collect_alerts, count_alerts, format_alert
from .reading import (
    parse_reading,
    read_alarm,
    read_node,
    read_sensor,
    read_sequence,
    read_value,
)
from .scan import count_out_of_range, first_out_of_range
from .scan import first_out_of_range as first_gap
from .tally import count_by_node, silent_nodes, unknown_nodes
from .window import board, moving_windows, snapshot

__version__ = "0.1.0"

__all__ = [
    "read_node", "read_sensor", "read_value", "read_sequence", "read_alarm",
    "parse_reading",
    "first_out_of_range", "count_out_of_range", "first_gap",
    "moving_windows", "board", "snapshot",
    "count_by_node", "silent_nodes", "unknown_nodes",
    "collect_alerts", "format_alert", "count_alerts",
]
