# s01e06 — make start | test | report
ROOT := ../..
PYTHON := $(if $(wildcard $(ROOT)/.venv/bin/python),$(abspath $(ROOT)/.venv/bin/python),python3)
.PHONY: start test report
start:
	@if [ -e artifacts/toolkit ]; then echo "artifacts/toolkit уже есть — не трогаю"; \
	else cp -R starter/toolkit artifacts/toolkit; echo "Создан artifacts/toolkit/"; fi
test:
	@$(PYTHON) -m pytest tests -q
report:
	@cd artifacts && $(PYTHON) -m toolkit ../data/day_sol019.txt
