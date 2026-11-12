"""s01e07 — проверка `toolkit/presence.py`.

Читать этот файл — законный ход: он и есть техническое задание. Тест не хранит
готовых ответов. Он генерирует потоки с фиксированным зерном генератора и
проверяет тождества множеств: молчащие и докладывающие не пересекаются и вместе
дают справочник, неизвестные лежат вне справочника, справочник после вызова
прежний, порядок прихода ничего не меняет.
"""

import random

import pytest
from testkit import load_artifact

REGISTRY = frozenset(f"{number:04d}" for number in range(1, 61))
HEARD = sorted(REGISTRY)[:45]


@pytest.fixture(scope="module")
def presence():
    return load_artifact(__file__, "toolkit/presence.py")


def make_stream(size, seed=20260911):
    """Поток пачками; '0000' шлёт чаще любого настоящего узла."""
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


def nodes_in(stream):
    return {reading[0] for reading in stream}


# Кто докладывает


def test_докладывающие_это_узлы_потока_без_повторов(presence):
    stream = make_stream(300)
    result = presence.reporting_nodes(stream)
    assert isinstance(result, (set, frozenset)), (
        f"reporting_nodes вернула {type(result).__name__}. Нужен set: повторов в ответе "
        "«кто докладывал» не бывает, порядок ничего не значит."
    )
    assert result == nodes_in(stream), (
        f"Докладывающих {len(result)}, а разных узлов в потоке {len(nodes_in(stream))}."
    )


def test_докладывающие_не_зависят_от_порядка(presence):
    stream = make_stream(300)
    shuffled = list(stream)
    random.Random(5).shuffle(shuffled)
    assert presence.reporting_nodes(shuffled) == presence.reporting_nodes(stream)


def test_узел_с_единственным_пакетом_не_теряется(presence):
    stream = [("0042", "O2", 20.9, 1, False)] + make_stream(40)
    stream = [reading for reading in stream if reading[0] != "0042" or reading[3] == 1]
    assert "0042" in presence.reporting_nodes(stream), (
        "Узел 0042 прислал один пакет, первым в смене, и пропал из докладывающих."
    )


def test_на_пустом_потоке_никто_не_докладывает(presence):
    result = presence.reporting_nodes([])
    assert isinstance(result, (set, frozenset)) and not result, (
        f"На пустом потоке вернулось {result!r}. Пустое множество пишется set(), "
        "а {} — это пустой словарь."
    )


# Молчащие


def test_молчащие_и_докладывающие_делят_справочник(presence):
    stream = make_stream(200)
    silent = presence.silent_nodes(registry(), stream)
    heard = nodes_in(stream) & REGISTRY
    assert not (silent & heard), (
        f"Узлы {sorted(silent & heard)[:5]} и молчат, и докладывают одновременно."
    )
    assert silent | heard == REGISTRY, (
        "Молчащие вместе с докладывающими должны дать весь справочник, не больше и не меньше."
    )


def test_молчащие_это_множество(presence):
    silent = presence.silent_nodes(registry(), make_stream(100))
    assert isinstance(silent, (set, frozenset)), (
        f"silent_nodes вернула {type(silent).__name__}, а нужен set."
    )


def test_молчащие_не_меняют_справочник(presence):
    shared = registry()
    presence.silent_nodes(shared, make_stream(200))
    assert shared == REGISTRY, (
        f"После вызова в справочнике {len(shared)} узлов вместо {len(REGISTRY)}. "
        "`registry -= ...` меняет тот самый объект, что передал вызывающий."
    )


def test_молчащие_работают_и_с_frozenset(presence):
    stream = make_stream(200)
    assert presence.silent_nodes(REGISTRY, stream) == presence.silent_nodes(registry(), stream), (
        "Со справочником-frozenset ответ должен быть тем же, что с обычным множеством."
    )


def test_на_пустом_потоке_молчат_все(presence):
    assert presence.silent_nodes(registry(), []) == REGISTRY


# Неизвестные


def test_неизвестные_это_узлы_вне_справочника(presence):
    stream = make_stream(200)
    unknown = presence.unknown_nodes(registry(), stream)
    assert unknown == {"0000"}, (
        f"Неизвестные узлы: {unknown!r}. В этом потоке вне справочника только '0000'."
    )
    assert not (unknown & REGISTRY), "Неизвестный узел не может быть в справочнике."


def test_неизвестные_это_множество(presence):
    unknown = presence.unknown_nodes(registry(), make_stream(100))
    assert isinstance(unknown, (set, frozenset)), (
        f"unknown_nodes вернула {type(unknown).__name__}, а нужен set."
    )


def test_неизвестные_не_меняют_справочник(presence):
    shared = registry()
    presence.unknown_nodes(shared, make_stream(200))
    assert shared == REGISTRY, (
        f"После вызова в справочнике {len(shared)} узлов вместо {len(REGISTRY)}: в него "
        "что-то добавили или из него что-то убрали."
    )


def test_на_пустом_потоке_неизвестных_нет(presence):
    unknown = presence.unknown_nodes(registry(), [])
    assert unknown == set(), f"На пустом потоке вернулось {unknown!r}."


# Все три вместе


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_три_ответа_согласованы(presence, seed):
    stream = make_stream(150, seed=seed)
    heard = presence.reporting_nodes(stream)
    silent = presence.silent_nodes(registry(), stream)
    unknown = presence.unknown_nodes(registry(), stream)
    assert heard == (REGISTRY - silent) | unknown, (
        "Докладывающие должны быть ровно «справочник без молчащих» плюс неизвестные: "
        "три функции противоречат друг другу."
    )
