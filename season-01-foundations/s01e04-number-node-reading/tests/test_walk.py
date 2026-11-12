"""s01e04 — проверка `toolkit/walk.py`.

Читать этот файл — законный ход: он и есть техническое задание. Тест не сверяет
ответ с готовой таблицей. Он генерирует потоки с фиксированным зерном генератора,
с множеством равных показаний, и проверяет свойства: порядок, устойчивость при
равных значениях, неизменность входа, отсутствие потерянных пар.
"""

import random

import pytest
from testkit import load_artifact

SEEDS = [3, 214, 1187, 20261112]


@pytest.fixture(scope="module")
def walk():
    return load_artifact(__file__, "toolkit/walk.py")


def make_stream(seed, size=60):
    """Поток пакетов, где значения часто совпадают: показания с шагом 0.5."""
    rng = random.Random(seed)
    stream = []
    for sequence in range(1, size + 1):
        node = str(rng.randint(1, 40)).zfill(4)
        value = 96.0 + rng.randint(0, 16) / 2
        stream.append((node, "P", value, sequence, False))
    return stream


def positions(stream):
    """Порядок прихода каждого пакета: его номер стоит в четвёртом поле."""
    return [reading[3] for reading in stream]


# worst


@pytest.mark.parametrize("seed", SEEDS)
def test_худшие_идут_по_убыванию(walk, seed):
    stream = make_stream(seed)
    result = walk.worst(stream, 10)
    values = [reading[2] for reading in result]
    assert len(result) == 10, f"Для n=10 вернулось {len(result)} пакетов."
    for left, right in zip(values, values[1:]):
        assert left >= right, f"Значения идут не по убыванию: {values}."


@pytest.mark.parametrize("seed", SEEDS)
def test_за_бортом_нет_значений_больше_отобранных(walk, seed):
    stream = make_stream(seed)
    result = walk.worst(stream, 7)
    lowest = min(reading[2] for reading in result)
    for reading in stream:
        if reading not in result:
            assert reading[2] <= lowest, (
                f"Пакет {reading} не попал в худшие, хотя его значение больше {lowest}."
            )


@pytest.mark.parametrize("seed", SEEDS)
def test_равные_значения_в_порядке_прихода(walk, seed):
    stream = make_stream(seed)
    result = walk.worst(stream, len(stream))
    for left, right in zip(result, result[1:]):
        if left[2] == right[2]:
            assert left[3] < right[3], (
                f"При равном значении {left[2]} пакет №{right[3]} оказался раньше "
                f"№{left[3]}. Сортировка обязана быть устойчивой: равные идут в "
                "порядке прихода. Сортируй по одному ключу — значению."
            )


def boundary_n(stream):
    """Наименьшее n, при котором граница отбора проходит внутри группы равных."""
    reference = sorted(stream, key=lambda reading: reading[2], reverse=True)
    for n in range(1, len(reference)):
        if reference[n - 1][2] == reference[n][2]:
            return n
    raise AssertionError("В потоке нет равных значений: тест не имел бы смысла")


@pytest.mark.parametrize("seed", SEEDS)
def test_на_границе_берутся_пришедшие_раньше(walk, seed):
    stream = make_stream(seed)
    n = boundary_n(stream)
    result = walk.worst(stream, n)
    cutoff = result[-1][2]
    taken = [reading[3] for reading in result if reading[2] == cutoff]
    left_out = [r[3] for r in stream if r[2] == cutoff and r not in result]
    assert left_out, "Самопроверка: на границе должны остаться равные за бортом."
    for number in left_out:
        assert number > max(taken), (
            f"На границе со значением {cutoff} взят пакет №{max(taken)}, а более "
            f"ранний №{number} — нет."
        )


@pytest.mark.parametrize("seed", SEEDS)
def test_худшие_не_меняют_вход(walk, seed):
    stream = make_stream(seed)
    before = list(stream)
    result = walk.worst(stream, 10)
    assert stream == before, (
        "После worst поток переупорядочен. sorted возвращает новый список, "
        "а list.sort() сортирует сам вход."
    )
    assert result is not stream


def test_все_равные_остаются_как_пришли(walk):
    stream = [("0042", "P", 100.0, number, False) for number in range(1, 9)]
    result = walk.worst(stream, 8)
    assert positions(result) == positions(stream), (
        f"Все значения равны, а порядок стал {positions(result)}."
    )


@pytest.mark.parametrize(("n", "expected"), [(0, 0), (3, 3), (100, 60)])
def test_сколько_просили_столько_и_дали(walk, n, expected):
    result = walk.worst(make_stream(7), n)
    assert type(result) is list and len(result) == expected, (
        f"worst(поток из 60, {n}) вернула {len(result) if isinstance(result, list) else result!r} "
        f"пакетов, а ждём {expected}."
    )


def test_короткий_поток_тоже_отсортирован(walk):
    stream = [("0001", "P", 97.0, 1, False), ("0002", "P", 103.5, 2, False)]
    result = walk.worst(stream, 10)
    assert positions(result) == [2, 1] and result is not stream, (
        f"Поток короче n, а вернулось {result!r}: его тоже надо отсортировать "
        "и вернуть новым списком."
    )


# numbered


@pytest.mark.parametrize("start", [1, 0, 101])
def test_номера_подряд_с_нужного(walk, start):
    stream = make_stream(11, size=5)
    result = walk.numbered(stream, start)
    numbers = [pair[0] for pair in result]
    assert numbers == list(range(start, start + 5)), (
        f"numbered(..., start={start}) дала номера {numbers}."
    )


def test_по_умолчанию_с_единицы(walk):
    result = walk.numbered(make_stream(11, size=3))
    assert [pair[0] for pair in result] == [1, 2, 3], (
        f"Без start номера {[pair[0] for pair in result]}, а в отчёте счёт с единицы."
    )


def test_пакеты_те_же_и_в_том_же_порядке(walk):
    stream = make_stream(11, size=6)
    result = walk.numbered(stream)
    assert type(result) is list and len(result) == len(stream)
    for pair, reading in zip(result, stream):
        assert pair[1] is reading, (
            f"Вторым элементом пары должен быть сам пакет, а вернулось {pair[1]!r}."
        )


def test_пустой_поток_без_номеров(walk):
    assert walk.numbered([]) == []


# pair_up


def test_пары_сходятся_с_входом(walk):
    nodes = ["0042", "1187", "2210"]
    values = [101.5, 95.8, 104.0]
    result = walk.pair_up(nodes, values)
    assert result == [("0042", 101.5), ("1187", 95.8), ("2210", 104.0)], (
        f"Вернулось {result!r}: пара — (узел, значение), в порядке списков."
    )


@pytest.mark.parametrize(
    ("nodes", "values"),
    [(["0042", "1187", "2210"], [101.5, 95.8]), (["0042"], [101.5, 95.8, 104.0])],
)
def test_разная_длина_это_ошибка(walk, nodes, values):
    with pytest.raises(ValueError):
        result = walk.pair_up(nodes, values)
        pytest.fail(
            f"Списки длиной {len(nodes)} и {len(values)} дали {result!r}. Хвост "
            "потерян молча; нужен zip(..., strict=True), чтобы об этом узнали."
        )


# extremes


def test_пустой_поток_это_none(walk):
    result = walk.extremes([])
    assert result is None, (
        f"Для пустого потока вернулось {result!r}. Ни наименьшего, ни наибольшего нет: None."
    )


@pytest.mark.parametrize("seed", SEEDS)
def test_крайние_значения_ограничивают_поток(walk, seed):
    stream = make_stream(seed)
    low, high = walk.extremes(stream)
    for reading in stream:
        assert low[2] <= reading[2] <= high[2], (
            f"Пакет {reading} вне ({low[2]}, {high[2]}): первым должен идти наименьший."
        )


@pytest.mark.parametrize("seed", SEEDS)
def test_крайние_согласованы_с_худшими(walk, seed):
    stream = make_stream(seed)
    low, high = walk.extremes(stream)
    top = walk.worst(stream, 1)[0]
    assert high is top, (
        f"extremes считает наибольшим пакет №{high[3]}, а worst — №{top[3]}. "
        "При равных значениях оба должны выбрать пришедший первым."
    )


def test_при_равенстве_крайним_берётся_первый(walk):
    stream = [
        ("0001", "P", 99.0, 1, False),
        ("0002", "P", 95.0, 2, False),
        ("0003", "P", 104.0, 3, False),
        ("0004", "P", 95.0, 4, False),
        ("0005", "P", 104.0, 5, False),
    ]
    low, high = walk.extremes(stream)
    assert (low[3], high[3]) == (2, 3), (
        f"Наименьший — №{low[3]}, наибольший — №{high[3]}. При равных значениях "
        "берётся пакет, пришедший первым: №2 и №3."
    )


def test_крайние_не_меняют_вход(walk):
    stream = make_stream(5)
    before = list(stream)
    walk.extremes(stream)
    assert stream == before, "После extremes поток переупорядочен: вход трогать нельзя."
