# s01e04 — make start | test
ROOT := ../..
PYTHON := $(if $(wildcard $(ROOT)/.venv/bin/python),$(abspath $(ROOT)/.venv/bin/python),python3)
.PHONY: start test
start:
	@mkdir -p artifacts/toolkit
	@if [ -e artifacts/toolkit/walk.py ]; then echo "artifacts/toolkit/walk.py уже есть — не трогаю"; \
	else cp starter.py artifacts/toolkit/walk.py; echo "Создан artifacts/toolkit/walk.py"; fi
test:
	@$(PYTHON) -m pytest tests -q
