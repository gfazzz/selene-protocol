# s01e08 — make start | test
ROOT := ../..
PYTHON := $(if $(wildcard $(ROOT)/.venv/bin/python),$(abspath $(ROOT)/.venv/bin/python),python3)
.PHONY: start test
start:
	@mkdir -p artifacts/toolkit
	@if [ -e artifacts/toolkit/logfile.py ]; then echo "artifacts/toolkit/logfile.py уже есть — не трогаю"; \
	else cp starter.py artifacts/toolkit/logfile.py; echo "Создан artifacts/toolkit/logfile.py"; fi
test:
	@$(PYTHON) -m pytest tests -q
