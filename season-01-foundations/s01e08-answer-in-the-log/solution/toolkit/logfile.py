"""toolkit/logfile.py — чтение журнала смены. Эталон s01e08."""


def read_log(path):
    lines = []
    with open(path, encoding="utf-8") as log:
        for line in log:
            line = line.rstrip("\n")
            if line.strip() != "":
                lines.append(line)
    return lines


def selene_answer(line):
    """Текст ответа, если строка — пакет с узла 0000, иначе None."""
    fields = line.split(";")
    if len(fields) == 5 and fields[0].strip() == "0000":
        return fields[1].strip()
    return None


def selene_answers(path):
    answers = []
    note = None
    for line in read_log(path):
        answer = selene_answer(line)
        if note is not None and answer is not None:
            answers.append((note, answer))
        if line.startswith("# "):
            note = line.removeprefix("# ")
        else:
            note = None
    return answers
