"""Неверное решение: окна строятся, съедая входной список."""
"""toolkit/window.py — окна, табло и снимки без общих списков. Эталон s01e05."""


def moving_windows(values, size):
    windows = []
    while len(values) >= size:
        window = []
        for offset in range(size):
            window.append(values[offset])
        windows.append(window)
        values.pop(0)
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
