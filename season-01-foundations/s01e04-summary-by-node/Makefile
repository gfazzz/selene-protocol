# s01e04 — make start | test
ROOT := ../..
PYTHON := $(if $(wildcard $(ROOT)/.venv/bin/python),$(abspath $(ROOT)/.venv/bin/python),python3)
.PHONY: start test
start:
	@mkdir -p artifacts/toolkit
	@if [ -e artifacts/toolkit/tally.py ]; then echo "artifacts/toolkit/tally.py уже есть — не трогаю"; \
	else cp starter.py artifacts/toolkit/tally.py; echo "Создан artifacts/toolkit/tally.py"; fi
test:
	@$(PYTHON) -m pytest tests -q
