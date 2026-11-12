"""Неверное решение: counts_once_per_node."""
"""toolkit/alerts.py — тревоги по пакетам телеметрии. Эталон s01e05."""


def collect_alerts(readings, low, high, found=None):
    if found is None:
        found = []
    for reading in readings:
        node, sensor, value, sequence, alarm = reading
        if alarm or value < low or value > high:
            found.append(reading)
    return found


def format_alert(reading, prefix="ТРЕВОГА"):
    node, sensor, value, sequence, alarm = reading
    return f"{prefix} {node} {sensor} {value} #{sequence}"


def count_alerts(readings, low, high, counts=None):
    if counts is None:
        counts = {}
    for reading in collect_alerts(readings, low, high):
        node = reading[0]
        counts[node] = 1
    return counts
