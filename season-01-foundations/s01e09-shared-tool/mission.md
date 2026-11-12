```
╔══════════════════════════════════════════════════════════════╗
║  SELENE PROTOCOL · ЗАДАНИЕ s01e09                            ║
║  «Инструмент общего пользования»                             ║
╠══════════════════════════════════════════════════════════════╣
║  МЕСТО:    кратер Шеклтона, диспетчерская телеметрии         ║
║  ВРЕМЯ:    сол 19, 08:20                                     ║
║  ЗАКАЗЧИК: Окафор, диспетчер дневной смены                   ║
║  ЗАТРАТЫ:  ~55 минут                                         ║
╚══════════════════════════════════════════════════════════════╝
```

## Обстановка

Пакет `toolkit` нужен дневной смене. Сейчас он при импорте печатает баннер в чужие
отчёты, пишет файл `toolkit.lock` в чужие каталоги и отдаёт наружу всё подряд.

## Приказ

Переписать `artifacts/toolkit/__init__.py`. Остальные файлы пакета не трогать: модули
`reading`, `labels`, `scan`, `walk`, `window`, `tally`, `presence`, `alerts` и
`__main__.py` уже готовы.

## Данные

Пакет и его публичные функции:

| Модуль | Функции |
|---|---|
| `reading` | `read_node`, `read_sensor`, `read_value`, `read_sequence`, `read_alarm`, `parse_reading` |
| `labels` | `normalize_code`, `format_reading`, `join_codes`, `field_note` |
| `scan` | `first_out_of_range`, `count_out_of_range`, `first_gap` |
| `walk` | `worst`, `numbered`, `pair_up`, `extremes` |
| `window` | `moving_windows`, `board`, `snapshot` |
| `tally` | `count_by_node`, `last_value_by_node`, `values_by_node` |
| `presence` | `reporting_nodes`, `silent_nodes`, `unknown_nodes` |
| `alerts` | `collect_alerts`, `format_alert`, `count_alerts` |

`data/day_sol019.txt` — утренние пакеты Окафор для `make report`.

## Критерии приёмки

- [ ] `import toolkit` ничего не печатает.
- [ ] `import toolkit` не создаёт файлов в текущем каталоге.
- [ ] `toolkit.__version__ == "0.1.0"`, строкой.
- [ ] `toolkit.__all__` перечисляет ровно двадцать девять функций из таблицы, без повторов.
- [ ] `from toolkit import *` даёт ровно имена из `__all__`.
- [ ] `toolkit.read_node is toolkit.reading.read_node` — и так для каждой функции.
- [ ] `python -m toolkit <файл>` печатает сводку первой строкой и не оставляет файлов.
- [ ] `make test` → 15 зелёных проверок.

## Выполнение

```bash
make start
make report
make test
```

Застрял — спроси SELENE в чате редактора. Она объяснит, но не напишет. Эталон — в
`solution/`, лучше после своей попытки.

## После выполнения

Пакет можно отдать дневной смене. Следующая серия разбирает, что Рейес делал с
ошибками, — и что из-за этого потерялось.
