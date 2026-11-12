# Материалы

**Стартовая библиография.** Здесь то, на что курс собирается опираться: книги,
статьи и исходники по сезонам. Когда серии будут написаны, этот файл станет
генерируемым — сводкой того, что реально процитировано в `theory.md` ста
семидесяти четырёх серий (так устроено в MOONLIGHT). Пока это список намерений, и он
короче будущего.

Пометки:
`[св]` — доступно бесплатно и легально;
`[б]` — уже лежит в библиотеке (OneDrive, «Библиотека программиста / Python,
Django» и «Библиотека / Программирование»).

---

## Как этим пользоваться

Список не для чтения подряд. Разумный порядок: проходишь серию — в `theory.md`
две-три позиции под конкретную тему — зацепило, читаешь оттуда.

Единственная книга, которую имеет смысл держать открытой параллельно всему
курсу, — Рамальо: она про то, чем Python отличается от «языка со скобками», и
её главы ложатся на сезоны 1–2 почти по порядку.

---

## Основа

Шесть позиций, которые понадобятся чаще всего.

| Книга | О чём | Где нужна |
|---|---|---|
| **Ramalho, «Fluent Python», 2-е изд.** `[б]` | модель данных языка, итераторы, дескрипторы, типизация | S1–S2, дальше как справочник |
| **Beazley, «Python Distilled»** (есть «Python Essential Reference» `[б]`) | язык без воды | S1–S2, S13 |
| **Лутц, «Изучаем Python» / «Learning Python», 6-е изд.** `[б]` | справочный слой: подробно и с историей | S1–S3 |
| **Kernighan & Pike, «Практика программирования»** | инженерные привычки, а не синтаксис | всегда |
| **Kleppmann, «Designing Data-Intensive Applications»** | данные, надёжность, согласованность | S3, S6–S8, S12 |
| **Hellmann, «The Python Standard Library by Example»** `[б]` | стандартная библиотека, на которой стоит весь курс | S1–S6, S12–S13 |

Из шести не хватает двух: Kernighan & Pike и Kleppmann. Обе стоят того, чтобы
завести, — вторая закрывает сразу четыре сезона.

---

## По сезонам

### Season 1–2 — Основы и питонизмы

- **Ramalho, «Fluent Python», 2-е изд.** `[б]`, гл. 1–2, 5–7, 14–17 — модель
  данных, функции, итераторы, контекстные менеджеры.
- **Beazley & Jones, «Python Cookbook», 3-е изд.** `[б]` — рецепты, каждый из
  которых объясняет приём.
- **Bader, «Python Tricks. The Book»** `[б]` — короткие сюжеты про то, что
  выглядит магией, пока не объяснено.
- **Danjou, «Serious Python»** `[б]` — упаковка, окружение, привычки.
- **Barry, «Head First Python», 2-е изд.** `[б]` — образец подачи, на который
  ссылается сама идея курса (см. [CREDITS.md](CREDITS.md)).
- **Документация CPython: `itertools`, `functools`, `contextlib`, `dataclasses`** `[св]`.
- **PEP 8, PEP 20, PEP 484** `[св]` — стиль, дзен, типизация.
- **Документация `argparse` и `sys`** `[св]` — командная строка и коды возврата (s01e12).
- **Okken, «Python Testing with pytest»** `[б]` — свои тесты (s02e14).
- **Hettinger, «Transforming Code into Beautiful, Idiomatic Python»** `[св]` —
  доклад, после которого код меняется.

### Season 3 — Данные

- **McKinney, «Python for Data Analysis», 3-е изд.** `[б]` `[св] онлайн` — от автора pandas.
- **RFC 4180** `[св]` — что такое CSV на самом деле и почему `split(',')` не работает.
- **Spolsky, «The Absolute Minimum Every Software Developer Must Know About Unicode»** `[св]` —
  кодировки до первой сломанной выгрузки.
- **База данных IANA tz и PEP 615 (`zoneinfo`)** `[св]` — время, пояса и почему
  «просто прибавить три часа» — ошибка.
- **«SQL as Understood by SQLite»** `[св]` — SQL по первоисточнику.
- **Kleppmann, гл. 2–3** — модели данных и форматы хранения, включая колоночные.

### Season 4 — Числа

- **VanderPlas, «Python Data Science Handbook»** `[б]` `[св]` — NumPy и векторизация практически.
- **Harris et al., «Array programming with NumPy», Nature 585 (2020)** `[св]` —
  устройство библиотеки от её авторов.
- **Goldberg, «What Every Computer Scientist Should Know About Floating-Point Arithmetic»** `[св]` —
  главный текст про вещественные числа.
- **Unpingco, «Python for Probability, Statistics, and Machine Learning»** `[б]` — статистика в коде.
- **Welford (1962) и устойчивые формулы дисперсии** `[св]` — почему наивная формула врёт.

### Season 5 — Деньги

- **PEP 327 и документация `decimal`** `[св]` — десятичная арифметика в Python.
- **IEEE 754-2019**, раздел про десятичные форматы — откуда `Decimal` берётся.
- **Fowler, «Patterns of Enterprise Application Architecture»** — шаблон Money
  и почему деньги не `float`.
- **Банковское округление (round half to even)** `[св]` — в стандарте и в
  документации `decimal`: почему «округляем как в школе» даёт систематическую
  ошибку в пользу одной стороны.

### Season 6 — Сеть и асинхронность

- **RFC 9110 (HTTP Semantics)** `[св]` — методы, идемпотентность, коды.
- **Nygard, «Release It!», 2-е изд.** — повторы, таймауты, предохранитель;
  книга, из которой в курс приходит половина сезона.
- **Fowler, «Python Concurrency with asyncio»** `[б]` (есть и по-русски) — основная книга сезона.
- **Beazley, «A Curious Course on Coroutines and Concurrency»** `[св]` — как
  устроено то, что потом назвали `async`.

### Season 7 — FastAPI

- **Документация FastAPI и Pydantic** `[св]` — редкий случай, когда документация
  и есть лучший учебник.
- **Спецификация ASGI** `[св]` — что именно вызывает сервер.
- **Tragura, «Building Python Microservices with FastAPI»** `[б]` — практика поверх документации.
- **Percival & Gregory, «Architecture Patterns with Python»** `[св] онлайн` —
  зависимости, границы, тестируемость сервиса.
- **OpenAPI Specification** `[св]` — схема как контракт, а не страница с примерами.
- **Документация Stripe об идемпотентности** `[св]` — образец того, как это делают в проде.

### Season 8 — Django

- **Документация Django: «Models», «Migrations», «Testing», «Auth»** `[св]` —
  первоисточник, и очень хороший.
- **Vincent, «Django for Professionals»** `[б]` — сборка проекта целиком; у него же
  «Django for APIs» `[б]` — для сравнения с Season 7.
- **Greenfeld & Roy, «Two Scoops of Django»** `[б]` — что делать не надо и почему.
- **Mele, «Django 5 by Example»** `[б]` — практические сценарии, включая права и админку.
- **Документация PostgreSQL, «Constraints»** `[св]` — ограничения в базе как
  предмет; читается и для SQLite.
- **Kleppmann, гл. 7** — транзакции и изоляция, чтобы «атомарно» перестало быть заклинанием.

### Season 9 — Машинное обучение

- **James, Witten, Hastie, Tibshirani, «An Introduction to Statistical Learning»** `[св]` —
  основной учебник сезона (в библиотеке его нет, и это первая позиция, которую
  стоит добавить).
- **Hastie, Tibshirani, Friedman, «The Elements of Statistical Learning»** `[св]` — то же глубже.
- **Domingos, «A Few Useful Things to Know about Machine Learning»** `[св]` —
  девять страниц, экономящих год.
- **Müller & Guido, «Introduction to Machine Learning with Python»** `[б]` —
  scikit-learn как эталон для сверки, а не как решение.
- **Unpingco** `[б]` — статистическая часть сезона.

### Season 10 — Языковые модели

- **Vaswani et al., «Attention Is All You Need» (2017)** `[св]` — первоисточник.
- **Karpathy, nanoGPT и «Let's build GPT: from scratch, in code, spelled out»** `[св]` —
  образец жанра, которому следует сезон.
- **Raschka, «Build a Large Language Model (From Scratch)»** — то же книгой и подробнее;
  в библиотеке нет, стоит завести под этот сезон.
- **Jurafsky & Martin, «Speech and Language Processing», 3-е изд.** `[св] черновик` —
  токенизация, языковые модели, оценка.
- **Sennrich et al., «Neural Machine Translation of Rare Words with Subword Units»** `[св]` — BPE.
- **Holtzman et al., «The Curious Case of Neural Text Degeneration»** `[св]` — откуда взялся `top-p`.
- **Bird, Klein, Loper, «Natural Language Processing with Python»** `[б]` — дотрансформерная
  обработка текста; полезна ровно как контраст.

### Season 11 — Чужая модель

- **Исходники [grok-1](https://github.com/xai-org/grok-1)** `[св]`, Apache 2.0 — предмет сезона.
- **Shazeer et al., «Outrageously Large Neural Networks» (2017)** `[св]` — разреженная смесь экспертов.
- **Fedus, Zoph, Shazeer, «Switch Transformers»** `[св]` — MoE, доведённая до практики.
- **Su et al., «RoFormer»** `[св]` — вращающиеся эмбеддинги (RoPE).
- **Ainslie et al., «GQA»** `[св]` — 48 голов запросов при 8 головах ключей.
- **Dettmers et al., «LLM.int8()»** `[св]` — квантование и его цена.
- **Hoffmann et al., «Training Compute-Optimal LLMs» (Chinchilla)** `[св]` —
  сколько это стоит и почему у колонии столько нет.

### Season 12 — Распределённое

- **Lamport, «Time, Clocks, and the Ordering of Events in a Distributed System»** `[св]` —
  1978 год, читается за вечер.
- **Ongaro & Ousterhout, «In Search of an Understandable Consensus Algorithm» (Raft)** `[св]` —
  согласование, которое реализуемо за сезон.
- **van Steen & Tanenbaum, «Distributed Systems», 4-е изд.** `[св]` — учебник целиком доступен.
- **Kleppmann, гл. 8–9** — что ломается и почему «сеть надёжна» — заблуждение №1.
- **Документация `multiprocessing` и `asyncio`** `[св]`.

### Season 13 — Производительность

- **Gorelick & Ozsvald, «High Performance Python», 2-е изд.** `[б]` — основная книга сезона.
- **Drepper, «What Every Programmer Should Know About Memory»** `[св]` — почему
  последовательный обход быстрее блуждания.
- **PEP 703 (свободнопоточный CPython) и PEP 659 (специализирующий интерпретатор)** `[св]` —
  что происходит с GIL и со скоростью прямо сейчас.
- **Документация `cProfile`, `tracemalloc`, `timeit`, `cffi`** `[св]`.
- **Okken, «Python Testing with pytest»** `[б]` — не про скорость, но про то, чем
  меряется весь курс; автору курса пригодится с первого сезона.

### Season 14 — Mojo

- **Modular, «Mojo Manual»** `[св]` — первоисточник; версия фиксируется вместе с SDK.
- **Lattner, доклады об MLIR и о происхождении Mojo** `[св]` — зачем язык появился.
- **Bryant & O'Hallaron, «Computer Systems: A Programmer's Perspective»**, гл. 5–6 —
  что делает код быстрым; без этого SIMD выглядит магией.
- **Agner Fog, «Optimizing software in C++» и таблицы инструкций** `[св]` — цена операций.
- **Документация NumPy об `ufunc` и трансляции** `[св]` — эталон, с которым сравниваемся.

Печатной книги по Mojo, которой стоило бы доверять, на момент написания нет:
язык меняется быстрее издательского цикла. Сезон пишется по документации и
проверяется кодом — и это отдельный аргумент в пользу того, чтобы учить в нём
концепты, а не синтаксис.

### Season 15 — Финальная операция

Новых источников нет: сезон прогоняет приёмку по всему, что было. Единственное
чтение — **Kernighan & Pike**, гл. 5–6 (отладка и тестирование) и собственные
`theory.md` четырнадцати сезонов.

---

## Чего в библиотеке не хватает

По убыванию пользы для курса: **Kleppmann** (четыре сезона), **ISLR**
`[св]` (весь Season 9), **Raschka, «Build a LLM from Scratch»** (Season 10),
**Nygard, «Release It!»** (Season 6), **Kernighan & Pike** (весь курс),
**Fowler, PoEAA** (Season 5). Бесплатно из этого списка доступна только ISLR
(и её старшая сестра ESL) — остальное придётся покупать; впрочем, Kleppmann
окупается быстрее прочих, потому что работает на четыре сезона сразу.
