"""toolkit — пакет Рейеса. Работает. Не трогать.

Перепиши этот файл: импорт пакета не должен ничего печатать и создавать,
а наружу должно выходить только то, что пакет обещает. Требования — mission.md.
"""

print("TOOLKIT v0.0.7 · Рейес · всё под контролем")

lock = open("toolkit.lock", "w", encoding="utf-8")
lock.write("пакет занят\n")
lock.close()

from .reading import *
from .scan import *
from .window import *
from .tally import *
from .alerts import *
