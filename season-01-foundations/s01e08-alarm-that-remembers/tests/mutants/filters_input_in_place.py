"""Неверное решение: filters_input_in_place."""
"""toolkit/alerts.py — тревоги по пакетам телеметрии. Эталон s01e08."""


def collect_alerts(readings, low, high, found=None):
    if found is None:
        found = []
    for reading in readings.copy():
        node, sensor, value, sequence, alarm = reading
        if alarm or value < low or value > high:
            found.append(reading)
        else:
            readings.remove(reading)
    return found


def format_alert(reading, prefix="ТРЕВОГА"):
    node, sensor, value, sequence, alarm = reading
    return f"{prefix} {node} {sensor} {value} #{sequence}"


def count_alerts(readings, low, high, counts=None):
    if counts is None:
        counts = {}
    for reading in collect_alerts(readings, low, high):
        node = reading[0]
        counts[node] = counts.get(node, 0) + 1
    return counts
