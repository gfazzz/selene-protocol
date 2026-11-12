# s01e02 — make start | test
ROOT := ../..
PYTHON := $(if $(wildcard $(ROOT)/.venv/bin/python),$(abspath $(ROOT)/.venv/bin/python),python3)
.PHONY: start test
start:
	@mkdir -p artifacts/toolkit
	@if [ -e artifacts/toolkit/scan.py ]; then echo "artifacts/toolkit/scan.py уже есть — не трогаю"; \
	else cp starter.py artifacts/toolkit/scan.py; echo "Создан artifacts/toolkit/scan.py"; fi
test:
	@$(PYTHON) -m pytest tests -q
