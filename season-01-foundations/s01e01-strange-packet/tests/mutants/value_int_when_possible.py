"""Неверное решение: value_int_when_possible."""
"""toolkit/reading.py — разбор одного пакета телеметрии. Эталон s01e01."""


def read_node(field):
    return field.strip()


def read_sensor(field):
    return field.strip()


def read_value(field):
    number = float(field)
    return int(number) if number == int(number) else number


def read_sequence(field):
    return int(field)


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
