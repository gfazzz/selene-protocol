"""s01e06 — проверка `toolkit/tally.py`.

Читать этот файл — законный ход: он и есть техническое задание. Тест не сверяет
сводку с готовой таблицей. Он генерирует потоки пакетов с фиксированным зерном
генератора и проверяет свойства: сумма счётчиков равна числу пакетов, сводка не
зависит от порядка прихода, последнее значение — по номеру, а не по приходу,
списки значений у узлов свои.
"""

import random

import pytest
from testkit import load_artifact

NODES = [f"{number:04d}" for number in range(1, 46)]


@pytest.fixture(scope="module")
def tally():
    return load_artifact(__file__, "toolkit/tally.py")


def make_stream(size, seed=20260909):
    """Поток пачками: узел часто шлёт несколько пакетов подряд, '0000' — чаще
    любого настоящего. Номера сквозные, каждый десятый пакет задержан в пути и
    приходит позже соседей."""
    rng = random.Random(seed)
    stream = []
    sequence = 1
    while len(stream) < size:
        node = "0000" if rng.random() < 0.2 else rng.choice(NODES)
        for _ in range(rng.randint(1, 4)):
            if len(stream) < size:
                value = round(rng.uniform(95.0, 105.0), 1)
                stream.append((node, "P", value, sequence, False))
                sequence += 1
    late = []
    on_time = []
    for index, reading in enumerate(stream):
        if index % 10 == 3:
            late.append(reading)
        else:
            on_time.append(reading)
    return on_time + late


def nodes_of(stream):
    seen = []
    for reading in stream:
        if reading[0] not in seen:
            seen.append(reading[0])
    return seen


# Счётчики


@pytest.mark.parametrize("size", [0, 1, 7, 500])
def test_сумма_счётчиков_равна_числу_пакетов(tally, size):
    stream = make_stream(size)
    counts = tally.count_by_node(stream)
    assert sum(counts.values()) == len(stream), (
        f"Счётчики дали {sum(counts.values())} пакетов, а в потоке их {len(stream)}. "
        "Каждый пакет должен быть сосчитан ровно один раз."
    )


def test_каждый_счётчик_совпадает_с_пересчётом(tally):
    stream = make_stream(300)
    counts = tally.count_by_node(stream)
    for node in nodes_of(stream):
        expected = sum(1 for reading in stream if reading[0] == node)
        assert counts.get(node) == expected, (
            f"Для узла {node} насчитано {counts.get(node)!r}, а пакетов от него {expected}."
        )
    assert sorted(counts) == sorted(nodes_of(stream)), (
        "В словаре должны быть ровно узлы из потока."
    )


def test_счётчики_не_зависят_от_порядка(tally):
    stream = make_stream(400)
    shuffled = list(stream)
    random.Random(7).shuffle(shuffled)
    original = tally.count_by_node(stream)
    assert type(original) is dict, f"count_by_node вернула {original!r}, а нужен словарь."
    assert tally.count_by_node(shuffled) == original, (
        "Тот же набор пакетов в другом порядке дал другую сводку."
    )


def test_ключи_это_строки_узлов(tally):
    counts = tally.count_by_node(make_stream(50))
    assert all(type(key) is str for key in counts), (
        f"Ключи сводки: {sorted(map(repr, counts))[:5]}… Номер узла — строка, как в s01e01."
    )


def test_пустой_поток_это_пустой_словарь(tally):
    counts = tally.count_by_node([])
    assert type(counts) is dict and counts == {}, (
        f"На пустом потоке вернулось {counts!r}. Сводка ничего — пустой словарь."
    )


# Последнее значение


def expected_last(stream):
    best = {}
    for node, sensor, value, sequence, alarm in stream:
        if node not in best or sequence > best[node][0]:
            best[node] = (sequence, value)
    return {node: pair[1] for node, pair in best.items()}


def test_последнее_значение_по_номеру_а_не_по_приходу(tally):
    stream = make_stream(300)
    result = tally.last_value_by_node(stream)
    expected = expected_last(stream)
    wrong = [node for node in expected if result.get(node) != expected[node]]
    assert not wrong, (
        f"У узлов {wrong[:5]} последнее значение не то. Задержанный пакет пришёл позже, "
        "но номер у него старый: последним считается пакет с наибольшим номером."
    )


def test_последнее_значение_не_зависит_от_порядка(tally):
    stream = make_stream(300)
    shuffled = list(stream)
    random.Random(11).shuffle(shuffled)
    assert tally.last_value_by_node(shuffled) == tally.last_value_by_node(stream), (
        "Тот же набор пакетов в другом порядке дал другие последние значения."
    )


def test_последние_значения_для_тех_же_узлов_что_и_счётчики(tally):
    stream = make_stream(200)
    result = tally.last_value_by_node(stream)
    assert type(result) is dict and sorted(result) == sorted(nodes_of(stream)), (
        f"Ключи: {sorted(result)[:5] if isinstance(result, dict) else result!r}. "
        "Последнее значение есть у каждого узла потока и только у них."
    )
    assert tally.last_value_by_node([]) == {}


# Значения по узлам


def test_значения_узла_в_порядке_прихода(tally):
    stream = make_stream(300)
    grouped = tally.values_by_node(stream)
    for node in nodes_of(stream):
        expected = [reading[2] for reading in stream if reading[0] == node]
        assert grouped.get(node) == expected, (
            f"Значения узла {node}: {grouped.get(node)!r}, а пришли {expected!r}. "
            "Нужны значения этого узла, все и в порядке прихода."
        )


def test_всех_значений_столько_же_сколько_пакетов(tally):
    stream = make_stream(250)
    grouped = tally.values_by_node(stream)
    assert type(grouped) is dict, f"values_by_node вернула {grouped!r}, а нужен словарь."
    assert sum(len(values) for values in grouped.values()) == len(stream), (
        "Значений во всех списках вместе не столько, сколько пакетов."
    )


def test_у_каждого_узла_свой_список(tally):
    stream = make_stream(120)
    grouped = tally.values_by_node(stream)
    lists = list(grouped.values())
    for first in range(len(lists)):
        for second in range(first + 1, len(lists)):
            assert lists[first] is not lists[second], (
                "Два узла держат один и тот же список. `dict.fromkeys(узлы, [])` и "
                "общий `[]` в setdefault дают один объект на всех: s01e05 в новом месте."
            )
    node = nodes_of(stream)[0]
    before = {key: list(values) for key, values in grouped.items()}
    grouped[node].append(-1.0)
    others = [key for key in grouped if key != node and grouped[key] != before[key]]
    assert not others, f"Дописали значение узлу {node}, а изменились ещё {others[:3]}."


def test_вход_не_меняется(tally):
    stream = make_stream(150)
    copy = list(stream)
    tally.count_by_node(stream)
    tally.last_value_by_node(stream)
    tally.values_by_node(stream)
    assert stream == copy, "Сводка изменила поток, который ей передали."
