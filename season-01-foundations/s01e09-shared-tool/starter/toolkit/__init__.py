"""toolkit — пакет Рейеса. Работает. Не трогать.

Перепиши этот файл: импорт пакета не должен ничего печатать и создавать,
а наружу должно выходить только то, что пакет обещает. Требования — mission.md.
Запись в файл здесь — приём, файлы разбираются в s01e11.
"""

print("TOOLKIT v0.0.7 · Рейес · всё под контролем")

lock = open("toolkit.lock", "w", encoding="utf-8")
lock.write("пакет занят\n")
lock.close()

from .reading import *
from .labels import *
from .scan import *
from .walk import *
from .window import *
from .tally import *
from .presence import *
from .alerts import *
