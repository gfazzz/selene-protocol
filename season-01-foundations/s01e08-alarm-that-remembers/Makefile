# s01e05 — make start | test
ROOT := ../..
PYTHON := $(if $(wildcard $(ROOT)/.venv/bin/python),$(abspath $(ROOT)/.venv/bin/python),python3)
.PHONY: start test
start:
	@mkdir -p artifacts/toolkit
	@if [ -e artifacts/toolkit/alerts.py ]; then echo "artifacts/toolkit/alerts.py уже есть — не трогаю"; \
	else cp starter.py artifacts/toolkit/alerts.py; echo "Создан artifacts/toolkit/alerts.py"; fi
test:
	@$(PYTHON) -m pytest tests -q
