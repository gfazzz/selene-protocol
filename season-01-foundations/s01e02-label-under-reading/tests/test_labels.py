"""s01e02 — проверка `toolkit/labels.py`.

Читать этот файл — законный ход: он и есть техническое задание. Тест вызывает
функции на подготовленных значениях, включая краевые, и сравнивает строку
целиком: на табло важен каждый пробел.
"""

import pytest
from testkit import load_artifact


@pytest.fixture(scope="module")
def labels():
    return load_artifact(__file__, "toolkit/labels.py")


# Код датчика


@pytest.mark.parametrize(
    ("code", "expected"),
    [(" o2 ", "O2"), ("co2\n", "CO2"), ("P", "P"), ("\ttemp ", "TEMP")],
)
def test_код_без_краёв_и_заглавными(labels, code, expected):
    result = labels.normalize_code(code)
    assert result == expected, (
        f"normalize_code({code!r}) вернула {result!r}, а ждём {expected!r}. "
        "Нужны оба шага: убрать края и поднять регистр. Каждый метод возвращает "
        "новую строку, и результат первого надо отдать второму."
    )


def test_пробел_внутри_кода_остаётся(labels):
    result = labels.normalize_code(" temp in ")
    assert result == "TEMP IN", (
        f"Вернулось {result!r}. Убираются только края, середина кода — часть имени."
    )


# Подпись пакета


def test_подпись_по_образцу(labels):
    result = labels.format_reading("0214", "O2", 20.9, 118)
    assert result == "0214  O2       20.90  #000118", (
        f"Вернулось {result!r}.\nЖдём       '0214  O2       20.90  #000118'. "
        "Узел, два пробела, датчик в поле 6 по левому краю, значение в поле 8 по "
        "правому краю с двумя знаками, два пробела, '#' и номер в шесть цифр."
    )


def test_значение_без_хвоста_двоичной_дроби(labels):
    result = labels.format_reading("0214", "O2", 0.1 + 20.8, 118)
    assert result == "0214  O2       20.90  #000118", (
        f"Вернулось {result!r}. 0.1 + 20.8 в float — это 20.900000000000002: "
        "str() показывает всё, а точность .2f — два знака."
    )


@pytest.mark.parametrize(
    ("value", "column"),
    [(-3.5, "   -3.50"), (7, "    7.00"), (0.0, "    0.00"), (12345.678, "12345.68")],
)
def test_столбец_значения_ровно_восемь_знаков(labels, value, column):
    result = labels.format_reading("0042", "P", value, 7)
    expected = f"0042  P     {column}  #000007"
    assert result == expected, (
        f"format_reading(..., {value!r}, 7) вернула {result!r}, а ждём {expected!r}. "
        "Столбец значения — ширина 8, правый край, два знака после точки."
    )


def test_код_датчика_приводится(labels):
    result = labels.format_reading("0214", " o2 ", 20.9, 118)
    assert result == "0214  O2       20.90  #000118", (
        f"Вернулось {result!r}. Код датчика на табло проходит через normalize_code."
    )


def test_длинное_не_обрезается(labels):
    result = labels.format_reading("0733", "seed_t", 4.25, 1234567)
    assert result == "0733  SEED_T    4.25  #1234567", (
        f"Вернулось {result!r}. Ширина поля — минимум, а не потолок: длинный номер "
        "и длинный код выходят целиком. Обрезанный номер — это чужой пакет."
    )


def test_ширина_подписи_постоянна(labels):
    first = labels.format_reading("0214", "O2", 20.9, 118)
    second = labels.format_reading("3000", "CO2", -0.5, 5)
    assert len(first) == len(second) == 29, (
        f"Длины подписей {len(first)} и {len(second)}, а обе должны быть 29: "
        "иначе столбцы на табло разъезжаются."
    )


# Список кодов


@pytest.mark.parametrize(
    ("codes", "expected"),
    [(["O2", "P", "CO2"], "O2, P, CO2"), (["O2"], "O2"), ([], "")],
)
def test_коды_через_запятую(labels, codes, expected):
    result = labels.join_codes(codes)
    assert result == expected, (
        f"join_codes({codes!r}) вернула {result!r}, а ждём {expected!r}. "
        "Разделитель — запятая и пробел, и только между кодами."
    )


# Пометка для журнала


@pytest.mark.parametrize(
    ("name", "raw", "expected"),
    [
        ("value", "9,6", "поле value: '9,6'"),
        ("node", "0214 ", "поле node: '0214 '"),
        ("alarm", "1\n", "поле alarm: '1\\n'"),
        ("sensor", "it's", "поле sensor: \"it's\""),
    ],
)
def test_сырое_значение_видно_целиком(labels, name, raw, expected):
    result = labels.field_note(name, raw)
    assert result == expected, (
        f"field_note({name!r}, {raw!r}) вернула {result!r}, а ждём {expected!r}. "
        "Сырое значение показывают через !r: так видны кавычки, пробел в конце и "
        "перевод строки."
    )
