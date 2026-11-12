# s01e07 — make start | test
ROOT := ../..
PYTHON := $(if $(wildcard $(ROOT)/.venv/bin/python),$(abspath $(ROOT)/.venv/bin/python),python3)
.PHONY: start test
start:
	@mkdir -p artifacts/toolkit
	@if [ -e artifacts/toolkit/presence.py ]; then echo "artifacts/toolkit/presence.py уже есть — не трогаю"; \
	else cp starter.py artifacts/toolkit/presence.py; echo "Создан artifacts/toolkit/presence.py"; fi
test:
	@$(PYTHON) -m pytest tests -q
