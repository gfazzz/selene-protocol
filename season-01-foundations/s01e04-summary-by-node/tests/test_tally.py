"""s01e04 — проверка `toolkit/tally.py`.

Читать этот файл — законный ход: он и есть техническое задание. Тест не сверяет
сводку с готовой таблицей. Он генерирует потоки пакетов с фиксированным seed и
проверяет свойства: сумма счётчиков равна числу пакетов, результат не зависит от
порядка входа, молчащие и докладывающие узлы вместе дают справочник.
"""

import random

import pytest
from testkit import load_artifact

REGISTRY = frozenset(f"{number:04d}" for number in range(1, 61))
HEARD = sorted(REGISTRY)[:45]


@pytest.fixture(scope="module")
def tally():
    return load_artifact(__file__, "toolkit/tally.py")


def make_stream(size, seed=20260909):
    """Поток пакетов пачками: узел часто шлёт несколько пакетов подряд.
    Узел '0000' шлёт чаще любого настоящего — как в сюжете."""
    rng = random.Random(seed)
    stream = []
    sequence = 1
    while len(stream) < size:
        node = "0000" if rng.random() < 0.2 else rng.choice(HEARD)
        for _ in range(rng.randint(1, 4)):
            if len(stream) < size:
                stream.append((node, "O2", round(rng.uniform(19.5, 21.5), 2), sequence, False))
                sequence += 1
    return stream


def registry():
    """Свежая изменяемая копия справочника для каждого вызова."""
    return set(REGISTRY)


def reporting(stream):
    return {reading[0] for reading in stream}


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
    for node in reporting(stream):
        expected = sum(1 for reading in stream if reading[0] == node)
        assert counts.get(node) == expected, (
            f"Для узла {node} насчитано {counts.get(node)!r}, а пакетов от него {expected}."
        )
    assert set(counts) == reporting(stream), "В словаре должны быть ровно узлы из потока."


def test_результат_не_зависит_от_порядка(tally):
    stream = make_stream(400)
    shuffled = list(stream)
    random.Random(7).shuffle(shuffled)
    original = tally.count_by_node(stream)
    assert isinstance(original, dict), f"count_by_node вернула {original!r}, а нужен словарь."
    assert tally.count_by_node(shuffled) == original, (
        "Тот же набор пакетов в другом порядке дал другую сводку. Сводка зависит от "
        "того, какие пакеты пришли, а не от того, в каком порядке."
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


# Молчащие узлы


def test_молчащие_и_докладывающие_делят_справочник(tally):
    stream = make_stream(200)
    silent = tally.silent_nodes(registry(), stream)
    heard = reporting(stream) & REGISTRY
    assert not (silent & heard), (
        f"Узлы {sorted(silent & heard)[:5]} и молчат, и докладывают одновременно."
    )
    assert silent | heard == REGISTRY, (
        "Молчащие вместе с докладывающими должны дать весь справочник, не больше и не меньше."
    )


def test_молчащие_это_множество(tally):
    silent = tally.silent_nodes(registry(), make_stream(100))
    assert isinstance(silent, (set, frozenset)), (
        f"silent_nodes вернула {type(silent).__name__}. Нужен set: порядок здесь ничего "
        "не значит, а повторов быть не может."
    )


def test_молчащие_не_меняют_справочник(tally):
    shared = registry()
    tally.silent_nodes(shared, make_stream(200))
    assert shared == REGISTRY, (
        f"После вызова в справочнике {len(shared)} узлов вместо {len(REGISTRY)}. "
        "`registry -= ...` меняет тот самый объект, что передал вызывающий."
    )


def test_на_пустом_потоке_молчат_все(tally):
    assert tally.silent_nodes(registry(), []) == REGISTRY


# Неизвестные узлы


def test_неизвестные_это_узлы_вне_справочника(tally):
    stream = make_stream(200)
    unknown = tally.unknown_nodes(registry(), stream)
    assert unknown == {"0000"}, (
        f"Неизвестные узлы: {unknown!r}. В этом потоке вне справочника только '0000'."
    )
    assert not (unknown & REGISTRY), "Неизвестный узел не может быть в справочнике."


def test_неизвестные_это_множество(tally):
    unknown = tally.unknown_nodes(registry(), make_stream(100))
    assert isinstance(unknown, (set, frozenset)), (
        f"unknown_nodes вернула {type(unknown).__name__}, а нужен set."
    )


def test_неизвестные_не_меняют_справочник(tally):
    shared = registry()
    tally.unknown_nodes(shared, make_stream(200))
    assert shared == REGISTRY, (
        f"После вызова в справочнике {len(shared)} узлов вместо {len(REGISTRY)}: в него "
        "что-то добавили или из него что-то убрали."
    )


def test_на_пустом_потоке_неизвестных_нет(tally):
    unknown = tally.unknown_nodes(registry(), [])
    assert unknown == set(), f"На пустом потоке вернулось {unknown!r}."
