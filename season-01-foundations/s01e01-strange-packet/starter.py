"""toolkit/reading.py — разбор одного пакета телеметрии.

Пакет — строка из пяти полей через точку с запятой:

    0214;O2;20.90;118;0
    узел;датчик;значение;номер;тревога

Заполни пять функций `read_*`. Каждая получает одно поле — строку — и возвращает
значение нужного типа. Сейчас они возвращают None, поэтому тест красный.

`def`, `return` и `split` здесь просто приёмы записи: устройство функций разберём
в s01e05, распаковку и списки — в s01e03 и s02e01.
"""


def read_node(field):
    """Номер узла: '0214' → строка '0214'. Пробелы по краям не нужны."""
    return None


def read_sensor(field):
    """Код датчика: '  O2 ' → строка 'O2'. Пробелы внутри кода остаются."""
    return None


def read_value(field):
    """Показание: '20.90' → число с плавающей точкой."""
    return None


def read_sequence(field):
    """Номер пакета: '118' → целое. Дробный номер — ошибка, а не округление."""
    return None


def read_alarm(field):
    """Флаг тревоги: '1' → True, '0' → False. Пробелы по краям не важны."""
    return None


# Эта функция уже готова: она разрезает строку и зовёт твои пять.
def parse_reading(line):
    node, sensor, value, sequence, alarm = line.split(";")
    return (
        read_node(node),
        read_sensor(sensor),
        read_value(value),
        read_sequence(sequence),
        read_alarm(alarm),
    )
