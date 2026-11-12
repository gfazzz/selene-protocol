# s01e02 — make start | test
ROOT := ../..
PYTHON := $(if $(wildcard $(ROOT)/.venv/bin/python),$(abspath $(ROOT)/.venv/bin/python),python3)
.PHONY: start test
start:
	@mkdir -p artifacts/toolkit
	@if [ -e artifacts/toolkit/labels.py ]; then echo "artifacts/toolkit/labels.py уже есть — не трогаю"; \
	else cp starter.py artifacts/toolkit/labels.py; echo "Создан artifacts/toolkit/labels.py"; fi
test:
	@$(PYTHON) -m pytest tests -q
