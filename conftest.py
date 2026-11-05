"""Общая настройка проверок: версия Python и отчёт об источнике решения."""

import sys

import pytest

import testkit

MINIMUM_PYTHON = (3, 12)


def pytest_configure(config):
    if sys.version_info < MINIMUM_PYTHON:
        found = ".".join(map(str, sys.version_info[:3]))
        pytest.exit(f"Курсу нужен Python 3.12 или новее, найден {found}.", returncode=2)


def pytest_terminal_summary(terminalreporter):
    for line in testkit.source_report():
        terminalreporter.write_line(line)
