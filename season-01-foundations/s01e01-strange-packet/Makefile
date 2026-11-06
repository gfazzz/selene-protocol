# s01e01 — make start | test
ROOT := ../..
PYTHON := $(if $(wildcard $(ROOT)/.venv/bin/python),$(abspath $(ROOT)/.venv/bin/python),python3)
.PHONY: start test
start:
	@mkdir -p artifacts/toolkit
	@if [ -e artifacts/toolkit/reading.py ]; then echo "artifacts/toolkit/reading.py уже есть — не трогаю"; \
	else cp starter.py artifacts/toolkit/reading.py; echo "Создан artifacts/toolkit/reading.py"; fi
test:
	@$(PYTHON) -m pytest tests -q
