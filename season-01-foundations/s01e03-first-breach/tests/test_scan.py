"""s01e03 — проверка `toolkit/scan.py`.

Читать этот файл — законный ход: он и есть техническое задание. Тест вызывает
функции на подготовленных потоках — обычных, пустых, с нарушением в самом начале
и на самой границе — и сверяет результат и его тип.
"""

import pytest
from testkit import load_artifact

LOW, HIGH = 96, 104


@pytest.fixture(scope="module")
def scan():
    return load_artifact(__file__, "toolkit/scan.py")


# Первое нарушение


def test_нарушение_в_первом_пакете_даёт_индекс_ноль(scan):
    result = scan.first_out_of_range([95.8, 100.2, 101.0], LOW, HIGH)
    assert result == 0 and result is not None and result is not False, (
        f"Вернулось {result!r}. Нарушение в самом первом пакете — это индекс 0. "
        "Ноль — настоящий номер, а не «ничего не нашли»."
    )


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([100.0, 101.5, 104.6, 99.0], 2),
        ([100.0, 95.0, 110.0], 1),
        ([99.0, 99.5, 100.0, 120.0], 3),
    ],
)
def test_находит_первое_а_не_последнее(scan, values, expected):
    result = scan.first_out_of_range(values, LOW, HIGH)
    assert result == expected, (
        f"first_out_of_range({values!r}) вернула {result!r}, а первое нарушение "
        f"на позиции {expected}. Нашёл — выходи из цикла."
    )


def test_возвращает_индекс_а_не_значение(scan):
    result = scan.first_out_of_range([100.0, 100.0, 50.0], LOW, HIGH)
    assert result == 2 and type(result) is int, (
        f"Вернулось {result!r}. Нужен номер позиции (2), а не само показание."
    )


def test_границы_включены(scan):
    result = scan.first_out_of_range([96, 104, 96.0, 104.0, 100], LOW, HIGH)
    assert result is None, (
        f"Вернулось {result!r}, хотя 96 и 104 — допустимые значения: "
        "регламент включает границы. Проверь, где стоит < и где <=."
    )


def test_чуть_за_границей_это_нарушение(scan):
    assert scan.first_out_of_range([100, 104.01], LOW, HIGH) == 1
    assert scan.first_out_of_range([100, 95.99], LOW, HIGH) == 1


@pytest.mark.parametrize("values", [[], [100.0], [96, 100, 104]])
def test_нет_нарушений_это_None(scan, values):
    result = scan.first_out_of_range(values, LOW, HIGH)
    assert result is None, (
        f"first_out_of_range({values!r}) вернула {result!r}. «Не нашли» — это None: "
        "-1 и False похожи на ответ и легко проходят дальше как число."
    )


# Подсчёт


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([95.8, 100.2, 110.0, 101.0, 50.0], 3),
        ([96, 104, 100], 0),
        ([95.99, 104.01], 2),
        ([], 0),
    ],
)
def test_считает_нарушения_с_обеих_сторон(scan, values, expected):
    result = scan.count_out_of_range(values, LOW, HIGH)
    assert type(result) is int and result == expected, (
        f"count_out_of_range({values!r}) вернула {result!r}, а нарушений {expected}. "
        "Считаются выходы и вниз, и вверх; границы допустимы."
    )


def test_подсчёт_согласован_с_поиском(scan):
    values = [100.0, 99.0, 103.9, 96.0]
    assert scan.count_out_of_range(values, LOW, HIGH) == 0
    assert scan.first_out_of_range(values, LOW, HIGH) is None


# Пропуски номеров


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [([5, 6, 8], 7), ([5, 8], 6), ([1, 2, 4, 5, 7], 3), ([117, 118, 120, 121], 119)],
)
def test_первый_пропущенный_номер(scan, numbers, expected):
    result = scan.first_gap(numbers)
    assert result == expected, (
        f"first_gap({numbers!r}) вернула {result!r}, а первым пропущен {expected}. "
        "Нужен сам пропущенный номер, и только первый."
    )


@pytest.mark.parametrize("numbers", [[], [42], [5, 6, 7], [0, 1]])
def test_без_пропусков_это_None(scan, numbers):
    result = scan.first_gap(numbers)
    assert result is None, (
        f"first_gap({numbers!r}) вернула {result!r}. Пропусков нет — ответ None. "
        "Пустой поток и поток из одного пакета тоже без пропусков."
    )


def test_пропуск_сразу_после_нуля(scan):
    result = scan.first_gap([0, 2, 3])
    assert result == 1, f"Вернулось {result!r}: после пакета 0 потерян пакет 1."
