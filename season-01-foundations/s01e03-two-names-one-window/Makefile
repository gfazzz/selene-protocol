# s01e03 — make start | test
ROOT := ../..
PYTHON := $(if $(wildcard $(ROOT)/.venv/bin/python),$(abspath $(ROOT)/.venv/bin/python),python3)
.PHONY: start test
start:
	@mkdir -p artifacts/toolkit
	@if [ -e artifacts/toolkit/window.py ]; then echo "artifacts/toolkit/window.py уже есть — не трогаю"; \
	else cp starter.py artifacts/toolkit/window.py; echo "Создан artifacts/toolkit/window.py"; fi
test:
	@$(PYTHON) -m pytest tests -q
