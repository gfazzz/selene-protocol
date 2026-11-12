"""s01e05 — проверка `toolkit/alerts.py`.

Читать этот файл — законный ход: он и есть техническое задание. Главное
свойство серии: функция не помнит прошлых вызовов. Тест вызывает её несколько
раз подряд, с разными данными, и требует, чтобы ни один вызов не видел следов
другого. Остальные проверки — на то, что именно считается тревогой.
"""

import random

import pytest
from testkit import load_artifact

LOW, HIGH = 96.0, 104.0

# Узел 2210: две тревоги — давление ниже предела и поднятый флаг.
NODE_2210 = [
    ("2210", "P", 91.2, 40, False),
    ("2210", "P", 99.8, 41, False),
    ("2210", "P", 100.1, 42, True),
]
# Узел 0042: всё в норме.
NODE_0042 = [
    ("0042", "P", 100.4, 7, False),
    ("0042", "P", 99.9, 8, False),
]


@pytest.fixture(scope="module")
def alerts():
    return load_artifact(__file__, "toolkit/alerts.py")


def make_readings(seed, count):
    """Случайные пакеты с фиксированным seed: повторный прогон даёт то же самое."""
    rng = random.Random(seed)
    nodes = ["0042", "0214", "1187", "2210"]
    readings = []
    for sequence in range(count):
        value = round(rng.uniform(90.0, 110.0), 1)
        readings.append((rng.choice(nodes), "P", value, sequence, rng.random() < 0.1))
    return readings


# Что считается тревогой


def test_тревоги_узла_2210(alerts):
    result = alerts.collect_alerts(NODE_2210, LOW, HIGH)
    assert result == [NODE_2210[0], NODE_2210[2]], (
        f"Вернулось {result!r}. Тревога — значение вне [low, high] или поднятый флаг; "
        "порядок исходный."
    )


def test_границы_допустимы(alerts):
    readings = [("0042", "P", 96.0, 1, False), ("0042", "P", 104.0, 2, False)]
    result = alerts.collect_alerts(readings, LOW, HIGH)
    assert result == [], (
        f"Вернулось {result!r}. 96 и 104 — допустимые значения: границы включены."
    )


def test_флаг_тревоги_сам_по_себе_тревога(alerts):
    readings = [("0042", "O2", 20.9, 3, True)]
    result = alerts.collect_alerts(readings, 19.5, 23.5)
    assert result == readings, (
        f"Вернулось {result!r}. Значение в норме, но флаг поднят — это тревога."
    )


def test_вход_не_меняется(alerts):
    readings = make_readings(1, 40)
    before = list(readings)
    result = alerts.collect_alerts(readings, LOW, HIGH)
    assert type(result) is list, f"collect_alerts вернула {result!r}, а ждём список."
    assert readings == before, (
        "collect_alerts изменила список пакетов, который ей передали. Функция "
        "отвечает на вопрос и не трогает то, о чём её спросили."
    )


# Свойство серии: вызовы не делят состояние


def test_второй_вызов_не_видит_первого(alerts):
    alerts.collect_alerts(NODE_2210, LOW, HIGH)
    result = alerts.collect_alerts(NODE_0042, LOW, HIGH)
    assert result == [], (
        f"Тревоги узла 0042: {result!r}, хотя у него всё в норме. Это тревоги из "
        "прошлого вызова. Значение по умолчанию вычисляется один раз, при def, и "
        "список-умолчание общий для всех вызовов. Используй None как маркер."
    )


def test_каждый_вызов_возвращает_новый_список(alerts):
    first = alerts.collect_alerts(NODE_0042, LOW, HIGH)
    second = alerts.collect_alerts(NODE_0042, LOW, HIGH)
    assert first == [] and second == []
    assert first is not second, (
        "Два вызова без found вернули один и тот же список. Вызывающий, который "
        "допишет в свой результат, испортит результат соседа."
    )


def test_повтор_даёт_тот_же_ответ(alerts):
    readings = make_readings(7, 60)
    result = alerts.collect_alerts(readings, LOW, HIGH)
    assert type(result) is list, f"collect_alerts вернула {result!r}, а ждём список."
    first = list(result)  # копия: если функция вернёт тот же список, он не изменится
    second = alerts.collect_alerts(readings, LOW, HIGH)
    assert first == second, (
        f"Тот же вопрос дважды — {len(first)} и {len(second)} тревог. Функция что-то "
        "копит между вызовами."
    )


@pytest.mark.parametrize("seed", [11, 12, 13])
def test_по_частям_то_же_что_целиком(alerts, seed):
    readings = make_readings(seed, 80)
    head, tail = [], []
    for index in range(len(readings)):
        (head if index < 30 else tail).append(readings[index])
    whole = alerts.collect_alerts(readings, LOW, HIGH)
    assert type(whole) is list and whole, f"collect_alerts вернула {whole!r}."
    found = alerts.collect_alerts(head, LOW, HIGH)
    alerts.collect_alerts(tail, LOW, HIGH, found)
    assert found == whole, (
        "Тревоги по частям, собранные в один found, не совпали с тревогами по всему "
        "списку сразу."
    )


# Переданный found дополняется, а не заменяется


def test_переданный_список_дополняется_и_возвращается(alerts):
    found = [("0001", "P", 80.0, 1, True)]
    result = alerts.collect_alerts(NODE_2210, LOW, HIGH, found)
    assert result is found, (
        "С переданным found функция вернула другой список. Договорённость: дописать "
        "в переданный и вернуть его же."
    )
    assert found == [("0001", "P", 80.0, 1, True), NODE_2210[0], NODE_2210[2]], (
        f"В found оказалось {found!r}: прежнее содержимое должно остаться в начале."
    )


def test_пустой_переданный_список_тоже_тот_же_объект(alerts):
    found = []
    result = alerts.collect_alerts(NODE_2210, LOW, HIGH, found=found)
    assert result is found and len(found) == 2, (
        "Передан пустой список, а вернулся другой. Пустой список ложен, поэтому "
        "`found or []` его подменяет. Проверять надо «не передано», то есть is None."
    )


# Строка тревоги


def test_строка_тревоги_по_умолчанию(alerts):
    result = alerts.format_alert(("0214", "P", 91.2, 118, False))
    assert result == "ТРЕВОГА 0214 P 91.2 #118", f"Вернулось {result!r}."


def test_префикс_передаётся_по_имени_и_не_залипает(alerts):
    reading = ("0214", "P", 91.2, 118, False)
    named = alerts.format_alert(reading, prefix="СБОЙ")
    positional = alerts.format_alert(reading, "ПРОВЕРКА")
    again = alerts.format_alert(reading)
    assert named == "СБОЙ 0214 P 91.2 #118", f"Вернулось {named!r}."
    assert positional == "ПРОВЕРКА 0214 P 91.2 #118", f"Вернулось {positional!r}."
    assert again == "ТРЕВОГА 0214 P 91.2 #118", (
        f"После вызова с другим префиксом без префикса вернулось {again!r}."
    )


# Счётчик тревог


def test_счётчик_по_узлам(alerts):
    result = alerts.count_alerts(NODE_2210 + NODE_0042, LOW, HIGH)
    assert result == {"2210": 2}, (
        f"Вернулось {result!r}. У 2210 две тревоги; у 0042 ни одной, и в словаре "
        "его нет совсем."
    )


def test_счётчик_не_помнит_прошлого_вызова(alerts):
    alerts.count_alerts(NODE_2210, LOW, HIGH)
    result = alerts.count_alerts(NODE_2210, LOW, HIGH)
    assert result == {"2210": 2}, (
        f"Второй вызов насчитал {result!r}. Словарь-умолчание общий для всех вызовов, "
        "как и список."
    )


def test_переданный_счётчик_дополняется(alerts):
    counts = {"2210": 5, "0001": 1}
    result = alerts.count_alerts(NODE_2210, LOW, HIGH, counts)
    assert result is counts and counts == {"2210": 7, "0001": 1}, (
        f"Вернулось {result!r}. Переданный словарь дополняется: к пяти прежним "
        "тревогам 2210 прибавляются две новые."
    )


@pytest.mark.parametrize("seed", [21, 22])
def test_сумма_счётчика_равна_числу_тревог(alerts, seed):
    readings = make_readings(seed, 100)
    counts = alerts.count_alerts(readings, LOW, HIGH)
    total = 0
    for node in counts:
        total = total + counts[node]
    assert total == len(alerts.collect_alerts(readings, LOW, HIGH)), (
        "Сумма по узлам не равна числу тревог: тревога потерялась или посчитана дважды."
    )
