"""s01e10 — проверка `toolkit/errors.py`.

Читать этот файл — законный ход: он и есть техническое задание. Ось серии —
поведение при отказе: плохая запись обязана дать конкретную ошибку с именем
поля и сохранённой причиной, а чужая ошибка не должна теряться по дороге.
"""

import pytest
from testkit import load_artifact


@pytest.fixture(scope="module")
def errors():
    return load_artifact(__file__, "toolkit/errors.py")


def raised_by(errors, line):
    """Возвращает ошибку TelemetryError, которую подняла parse_strict(line)."""
    with pytest.raises(errors.TelemetryError) as caught:
        result = errors.parse_strict(line)
        pytest.fail(f"parse_strict({line!r}) вернула {result!r}, а должна была поднять BadPacket.")
    return caught.value


# Разбор хорошего пакета


def test_хороший_пакет_разбирается(errors):
    result = errors.parse_strict(" 0214 ; O2 ;20.90;118;0\n")
    assert result == ("0214", "O2", pytest.approx(20.9), 118, False), (
        f"Хороший пакет разобран как {result!r}. Строгий разбор не должен "
        "ломать то, что работало в s01e01."
    )
    assert type(result[3]) is int and type(result[4]) is bool


def test_пробелы_вокруг_флага_не_важны(errors):
    result = errors.parse_strict("0214;O2;20.90;118; 1 ")
    assert result[4] is True, f"Флаг ' 1 ' разобран как {result[4]!r}, а ждём True."


# Плохие поля: какая ошибка и что в ней


def test_запятая_в_показании_это_BadPacket_поля_value(errors):
    err = raised_by(errors, "0733;P;9,6;5521;1")
    assert isinstance(err, errors.BadPacket), f"Поднялось {type(err).__name__}, а ждём BadPacket."
    assert err.field == "value", (
        f"err.field = {err.field!r}. Вызывающему надо знать, какое поле плохое: 'value'."
    )
    assert "value" in str(err) and "9,6" in str(err), (
        f"Сообщение {str(err)!r} должно называть поле и показывать, что в нём было."
    )


def test_причина_ошибки_показания_сохранена(errors):
    err = raised_by(errors, "0733;P;9,6;5521;1")
    assert isinstance(err.__cause__, ValueError), (
        f"__cause__ = {err.__cause__!r}. Исходный ValueError должен остаться причиной: "
        "raise BadPacket(...) from err."
    )


def test_дробный_номер_это_BadPacket_поля_sequence(errors):
    err = raised_by(errors, "0214;O2;20.90;12.5;0")
    assert isinstance(err, errors.BadPacket) and err.field == "sequence", (
        f"Поднялось {type(err).__name__} с field={getattr(err, 'field', None)!r}, "
        "а ждём BadPacket с field='sequence'."
    )
    assert isinstance(err.__cause__, ValueError), "Причина ошибки номера потеряна."


@pytest.mark.parametrize("flag", ["2", "", "да", "true"])
def test_неизвестный_флаг_это_BadPacket_поля_alarm(errors, flag):
    err = raised_by(errors, f"0214;O2;20.90;118;{flag}")
    assert isinstance(err, errors.BadPacket) and err.field == "alarm", (
        f"Флаг {flag!r}: поднялось {type(err).__name__} с field={getattr(err, 'field', None)!r}. "
        "Флаг бывает только '0' или '1', остальное — плохой пакет, а не «нет тревоги»."
    )


@pytest.mark.parametrize("line", ["0214;O2;20.90;118", "0214;O2;20.90;118;0;лишнее", ""])
def test_не_пять_полей_это_BadPacket_без_поля(errors, line):
    err = raised_by(errors, line)
    assert isinstance(err, errors.BadPacket) and err.field is None, (
        f"Строка {line!r}: поднялось {type(err).__name__} с field={getattr(err, 'field', None)!r}. "
        "Сломана сама строка, а не одно поле, поэтому field=None."
    )


# Разбор потока


LINES = [
    "0214;O2;20.90;118;0",
    "0733;P;9,6;5521;1",
    "1187;P;99.80;119;0",
    "0042;T;21.4;120;7",
    "0000;SELENE;0.00;121;0",
]


def test_поток_принятые_и_отклонённые(errors):
    accepted, rejected = errors.parse_all(LINES)
    nodes = [packet[0] for packet in accepted]
    assert nodes == ["0214", "1187", "0000"], f"Приняты пакеты узлов {nodes}, ждём 0214, 1187, 0000."
    numbers = [number for number, _ in rejected]
    assert numbers == [2, 4], (
        f"Отклонены строки {numbers}, ждём [2, 4]: номер строки считают с 1, как в журнале."
    )
    assert len(accepted) + len(rejected) == len(LINES), "Принято + отклонено должно быть = всего."


def test_отклонённая_строка_несёт_свою_ошибку(errors):
    _, rejected = errors.parse_all(LINES)
    assert rejected, "Отклонённых нет. Авария в строке 2 снова пропала молча."
    fields = [err.field for _, err in rejected]
    assert fields == ["value", "alarm"], (
        f"Поля отклонённых строк: {fields}. Каждой строке — её ошибка, а не общая «что-то не так»."
    )


@pytest.mark.parametrize("intruder", [None, 42])
def test_чужая_ошибка_не_проглатывается(errors, intruder):
    lines = ["0214;O2;20.90;118;0", intruder, "1187;P;99.80;119;0"]
    with pytest.raises((AttributeError, TypeError)):
        result = errors.parse_all(lines)
        pytest.fail(
            f"parse_all на {intruder!r} вместо строки вернула {result!r}. Это не плохой пакет, "
            "а ошибка в вызывающем коде: её нельзя ловить вместе с BadPacket."
        )
