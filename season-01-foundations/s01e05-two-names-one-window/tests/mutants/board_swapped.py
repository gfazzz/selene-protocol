"""Неверное решение: перепутаны строки и столбцы."""
"""toolkit/window.py — окна, табло и снимки без общих списков. Эталон s01e05."""


def moving_windows(values, size):
    windows = []
    start = 0
    while start + size <= len(values):
        window = []
        for offset in range(size):
            window.append(values[start + offset])
        windows.append(window)
        start = start + 1
    return windows


def board(rows, cols, fill):
    result = []
    for _ in range(cols):
        row = []
        for _ in range(rows):
            row.append(fill)
        result.append(row)
    return result


def snapshot(window):
    return tuple(window)
