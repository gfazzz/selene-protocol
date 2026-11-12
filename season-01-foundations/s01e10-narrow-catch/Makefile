# s01e07 — make start | test
ROOT := ../..
PYTHON := $(if $(wildcard $(ROOT)/.venv/bin/python),$(abspath $(ROOT)/.venv/bin/python),python3)
.PHONY: start test
start:
	@mkdir -p artifacts/toolkit
	@if [ -e artifacts/toolkit/errors.py ]; then echo "artifacts/toolkit/errors.py уже есть — не трогаю"; \
	else cp starter.py artifacts/toolkit/errors.py; echo "Создан artifacts/toolkit/errors.py"; fi
test:
	@$(PYTHON) -m pytest tests -q
