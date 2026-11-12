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
| `labels.py` | [s01e02](../s01e02-label-under-reading/README.md) |
| `scan.py` | [s01e03](../s01e03-first-breach/README.md) |
| `walk.py` | [s01e04](../s01e04-number-node-reading/README.md) |
| `window.py` | [s01e05](../s01e05-two-names-one-window/README.md) |
| `tally.py` | [s01e06](../s01e06-summary-by-node/README.md) |
| `presence.py` | [s01e07](../s01e07-who-is-silent/README.md) |
| `alerts.py` | [s01e08](../s01e08-alarm-that-remembers/README.md) |
| `__init__.py` (`__main__.py` дан готовым) | [s01e09](../s01e09-shared-tool/README.md) |
| `errors.py` | [s01e10](../s01e10-narrow-catch/README.md) |
| `logfile.py` | [s01e11](../s01e11-answer-in-the-log/README.md) |
| `cli.py` | [s01e12](../s01e12-one-command/README.md) |

Что проверяется — [`tests/test_toolkit.py`](tests/test_toolkit.py): импорт без
побочных эффектов, ни одна строка журнала не теряется, сводка по узлам и тревоги
сходятся между модулями, ответы SELENE находятся и повторяются, подписи и худшие
показания сходятся с потоком, `toolkit.cli` отвечает теми же ответами и сообщает
об ошибке кодом возврата.

`toolkit` продолжается в Season 2: там те же модули получают срезы, генераторы,
классы и типы.
