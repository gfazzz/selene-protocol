# Season 1 — сквозной проект `toolkit`

Каждая серия сезона добавляет в `toolkit` один модуль. Здесь они собираются в
пакет и проверяются вместе: что приняла одна функция, то должно сойтись с тем,
что посчитала другая.

```bash
make project SEASON=01        # из корня курса
```

Сборка кладёт пакет в `build/`: сначала эталоны всех серий, поверх них твои файлы
из `artifacts/` каждой серии. Вывод сборки показывает, какие файлы взяты твои.
Ни одного своего — значит, проверяется эталон, и проект зелёный ещё до начала.

| Модуль | Серия |
|---|---|
| `reading.py` | [s01e01](../s01e01-strange-packet/README.md) |
| `scan.py` | [s01e02](../s01e02-first-breach/README.md) |
| `window.py` | [s01e03](../s01e03-two-names-one-window/README.md) |
| `tally.py` | [s01e04](../s01e04-summary-by-node/README.md) |
| `alerts.py` | [s01e05](../s01e05-alarm-that-remembers/README.md) |
| `__init__.py`, `__main__.py` | [s01e06](../s01e06-shared-tool/README.md) |
| `errors.py` | [s01e07](../s01e07-narrow-catch/README.md) |
| `logfile.py` | [s01e08](../s01e08-answer-in-the-log/README.md) |

Что проверяется — [`tests/test_toolkit.py`](tests/test_toolkit.py): импорт без
побочных эффектов, ни одна строка журнала не теряется, сводка по узлам и тревоги
сходятся между модулями, ответы SELENE находятся и повторяются, сводка работает из
командной строки.

`toolkit` продолжается в Season 2: там те же модули получают срезы, генераторы,
классы и типы.
