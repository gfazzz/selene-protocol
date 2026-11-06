"""Неверное решение: sequence_swallows_garbage."""
"""toolkit/reading.py — разбор одного пакета телеметрии. Эталон s01e01."""


def read_node(field):
    return field.strip()


def read_sensor(field):
    return field.strip()


def read_value(field):
    return float(field)


def read_sequence(field):
    try:
        return int(field)
    except ValueError:
        return 0


def read_alarm(field):
    return field.strip() == "1"


def parse_reading(line):
    node, sensor, value, sequence, alarm = line.split(";")
    return (
        read_node(node),
        read_sensor(sensor),
        read_value(value),
        read_sequence(sequence),
        read_alarm(alarm),
    )
