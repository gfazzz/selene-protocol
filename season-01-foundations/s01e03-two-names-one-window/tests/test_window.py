"""s01e03 — проверка `toolkit/window.py`.

Читать этот файл — законный ход: он и есть техническое задание. Тест проверяет
инварианты, а не текст решения: вызывает функцию, потом меняет то, что она
вернула (или то, что ей передали), и смотрит, не изменилось ли что-то ещё.
"""

import random

import pytest
from testkit import load_artifact


@pytest.fixture(scope="module")
def window():
    return load_artifact(__file__, "toolkit/window.py")


def pressures(count, seed):
    rng = random.Random(seed)
    return [round(rng.uniform(95.0, 105.0), 1) for _ in range(count)]


# Окна


@pytest.mark.parametrize(
    ("values", "size", "expected"),
    [
        ([1, 2, 3, 4], 2, [[1, 2], [2, 3], [3, 4]]),
        ([1, 2, 3, 4], 4, [[1, 2, 3, 4]]),
        ([1, 2, 3, 4], 1, [[1], [2], [3], [4]]),
        ([1, 2, 3], 5, []),
    ],
)
def test_окна_подряд(window, values, size, expected):
    result = window.moving_windows(values, size)
    assert result == expected, (
        f"moving_windows({values!r}, {size}) вернула {result!r}, а ждём {expected!r}."
    )


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_число_и_состав_окон_на_любых_данных(window, seed):
    values = pressures(40, seed)
    for size in (1, 3, 7, 40, 41):
        result = window.moving_windows(values, size)
        assert len(result) == max(0, len(values) - size + 1), (
            f"Окон длины {size} из {len(values)} значений: {len(result)}. "
            "Неполных окон в конце быть не должно, а последнее полное — должно."
        )
        for start, got in enumerate(result):
            for offset in range(size):
                assert got[offset] == values[start + offset], (
                    f"Окно №{start} при size={size} не совпадает с исходными данными."
                )


def test_входной_список_не_меняется(window):
    values = pressures(12, 7)
    before = list(values)
    window.moving_windows(values, 3)
    assert values == before, (
        "После moving_windows исходный список изменился. Функция получила не копию, "
        "а тот же список под другим именем: всё, что она с ним делает, видит вызывающий."
    )


def test_окна_это_разные_списки(window):
    result = window.moving_windows([1, 2, 3, 4, 5], 2)
    for i in range(len(result)):
        for j in range(i + 1, len(result)):
            assert result[i] is not result[j], (
                f"Окна №{i} и №{j} — один и тот же список (is). В результат добавлялся "
                "один список несколько раз."
            )


def test_правка_окна_не_трогает_соседей_и_вход(window):
    values = [10, 20, 30, 40]
    result = window.moving_windows(values, 2)
    result[0][1] = 999
    assert result[1] == [20, 30], (
        f"После правки окна №0 окно №1 стало {result[1]!r}. Окна делят элементы через "
        "общий список: соседнее окно не должно было измениться."
    )
    assert values == [10, 20, 30, 40], (
        f"После правки окна исходный список стал {values!r}: окно — это сам вход."
    )


def test_единственное_окно_не_сам_вход(window):
    values = [1, 2, 3]
    result = window.moving_windows(values, 3)
    assert result and result[0] is not values, (
        "Окно на всю длину — это сам входной список. Ему нужен свой список."
    )


# Табло


@pytest.mark.parametrize(("rows", "cols"), [(3, 4), (1, 4), (5, 2), (0, 3)])
def test_табло_нужного_размера(window, rows, cols):
    result = window.board(rows, cols, ".")
    assert len(result) == rows and all(row == ["."] * cols for row in result), (
        f"board({rows}, {cols}, '.') вернула {result!r}."
    )


def test_отметка_не_зажигает_столбец(window):
    result = window.board(4, 3, ".")
    result[0][1] = "X"
    column = [row[1] for row in result]
    assert column == ["X", ".", ".", "."], (
        f"Отметили одну ячейку, а столбец стал {column!r}. Строки табло — один и тот же "
        "список: ошибка Рейеса."
    )


def test_строки_табло_это_разные_списки(window):
    result = window.board(3, 2, 0)
    assert result[0] is not result[1] and result[1] is not result[2], (
        "Строки табло совпадают по is: это один список под несколькими именами."
    )


# Снимок


def test_снимок_это_кортеж_тех_же_значений(window):
    values = [101.2, 99.8, 100.4]
    result = window.snapshot(values)
    assert type(result) is tuple and result == (101.2, 99.8, 100.4), (
        f"snapshot вернула {result!r} типа {type(result).__name__}. Снимок — кортеж из "
        "элементов окна."
    )


def test_снимок_не_меняется_вместе_с_окном(window):
    values = [101.2, 99.8, 100.4]
    result = window.snapshot(values)
    values[0] = 0.0
    values.append(55.5)
    assert result == (101.2, 99.8, 100.4), (
        f"Окно изменили после снимка, и снимок стал {result!r}. Снимок держит ссылку на "
        "само окно, а не копирует его элементы."
    )
