"""Неверное решение: следующее окно — сдвиг предыдущего на месте."""
"""toolkit/window.py — окна, табло и снимки без общих списков. Эталон s01e03."""


def moving_windows(values, size):
    if size > len(values):
        return []
    window = []
    for offset in range(size):
        window.append(values[offset])
    windows = [window]
    for index in range(size, len(values)):
        window = windows[len(windows) - 1]
        window.pop(0)
        window.append(values[index])
        windows.append(window)
    return windows


def board(rows, cols, fill):
    result = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(fill)
        result.append(row)
    return result


def snapshot(window):
    return tuple(window)
