"""s01e01 — проверка `toolkit/reading.py`.

Читать этот файл — законный ход: он и есть техническое задание. Тест не смотрит
на текст решения. Он вызывает функции на подготовленных полях, включая краевые и
заведомо грязные, и сверяет значение и его тип.
"""

import pytest
from testkit import load_artifact


@pytest.fixture(scope="module")
def reading():
    return load_artifact(__file__, "toolkit/reading.py")


# Узел


@pytest.mark.parametrize("field", ["0214", "0000", "3000"])
def test_узел_остаётся_строкой_и_не_теряет_нули(reading, field):
    result = reading.read_node(field)
    assert type(result) is str and result == field, (
        f"read_node({field!r}) вернула {result!r}. Номер узла — имя, а не количество: "
        "его не складывают, а ноль в начале — часть имени."
    )


def test_узел_без_пробелов_по_краям(reading):
    result = reading.read_node("  0214\n")
    assert result == "0214", (
        f"Вернулось {result!r}. Строка неизменяема: strip() возвращает новую строку, "
        "а исходная остаётся какой была. Результат надо вернуть."
    )


# Датчик


def test_датчик_без_пробелов_по_краям(reading):
    result = reading.read_sensor("  O2 ")
    assert type(result) is str and result == "O2", (
        f"read_sensor('  O2 ') вернула {result!r}, а ждём 'O2'."
    )


def test_пробелы_внутри_кода_датчика_остаются(reading):
    result = reading.read_sensor(" ЕГО ЗОВУТ 0214 ")
    assert result == "ЕГО ЗОВУТ 0214", (
        f"Вернулось {result!r}. Убирать надо края, а не все пробелы подряд."
    )


# Показание


@pytest.mark.parametrize(
    ("field", "expected"),
    [("20.90", 20.9), ("-3.5", -3.5), (" 20.9 \n", 20.9), ("7", 7.0), ("0", 0.0)],
)
def test_показание_это_float(reading, field, expected):
    result = reading.read_value(field)
    assert type(result) is float, (
        f"read_value({field!r}) вернула {type(result).__name__}: {result!r}. "
        "Показание — число с плавающей точкой, даже если в поле нет точки."
    )
    assert result == pytest.approx(expected)


@pytest.mark.parametrize("field", ["абв", "", "20,90"])
def test_мусор_в_показании_это_ошибка(reading, field):
    with pytest.raises(ValueError):
        result = reading.read_value(field)
        pytest.fail(
            f"read_value({field!r}) вернула {result!r}. Придуманное показание опаснее "
            "ошибки: мусор должен дойти до вызывающего как ValueError."
        )


# Номер пакета


@pytest.mark.parametrize(("field", "expected"), [("118", 118), (" 118\n", 118), ("0", 0)])
def test_номер_пакета_это_int(reading, field, expected):
    result = reading.read_sequence(field)
    assert type(result) is int and result == expected, (
        f"read_sequence({field!r}) вернула {result!r} типа {type(result).__name__}. "
        "Номер — целое число."
    )


def test_большой_номер_не_искажается(reading):
    result = reading.read_sequence("9007199254740993")
    assert result == 9007199254740993, (
        f"Вернулось {result!r}, а в поле 9007199254740993. Путь через float теряет "
        "точность: у него 53 бита на мантиссу, у int ограничения нет."
    )


@pytest.mark.parametrize("field", ["12.5", "абв", ""])
def test_дробный_или_мусорный_номер_это_ошибка(reading, field):
    with pytest.raises(ValueError):
        result = reading.read_sequence(field)
        pytest.fail(
            f"read_sequence({field!r}) вернула {result!r}. Номер не округляют: пакета "
            "12.5 не существует, и об этом надо сообщить как ValueError."
        )


# Тревога


@pytest.mark.parametrize(
    ("field", "expected"), [("0", False), ("1", True), (" 0 ", False), (" 1\n", True)]
)
def test_флаг_тревоги_это_bool(reading, field, expected):
    result = reading.read_alarm(field)
    assert result is expected, (
        f"read_alarm({field!r}) вернула {result!r}, а ждём {expected!r}. Непустая строка "
        "истинна, включая '0': bool(field) здесь не помогает. Сравни содержимое поля."
    )


# Пакет целиком


def test_обычный_пакет(reading):
    result = reading.parse_reading("0214;O2;20.90;118;0\n")
    assert result == ("0214", "O2", pytest.approx(20.9), 118, False), (
        f"Пакет разобран как {result!r}."
    )


def test_странный_пакет_разбирается_по_тем_же_правилам(reading):
    result = reading.parse_reading("0000;ЕГО ЗОВУТ 0214;0.00;119;0")
    assert result == ("0000", "ЕГО ЗОВУТ 0214", pytest.approx(0.0), 119, False), (
        f"Пакет разобран как {result!r}."
    )
