"""Неверное решение: строки размножены умножением списка."""
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
    return [[fill] * cols] * rows


def snapshot(window):
    return tuple(window)
