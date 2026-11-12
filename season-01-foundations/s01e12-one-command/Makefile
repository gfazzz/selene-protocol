# s01e12 — make start | test | summary | answers
ROOT := ../..
PYTHON := $(if $(wildcard $(ROOT)/.venv/bin/python),$(abspath $(ROOT)/.venv/bin/python),python3)
LOGS := ../../s01e11-answer-in-the-log/data
.PHONY: start test summary answers
start:
	@if [ -e artifacts/toolkit ]; then echo "artifacts/toolkit уже есть — не трогаю"; \
	else cp -R starter/toolkit artifacts/toolkit; echo "Создан artifacts/toolkit/"; fi
test:
	@$(PYTHON) -m pytest tests -q
summary:
	@cd artifacts && $(PYTHON) -m toolkit.cli summary $(LOGS)/shift_sol038.log
answers:
	@cd artifacts && $(PYTHON) -m toolkit.cli answers $(LOGS)/shift_rejes_first.log $(LOGS)/shift_rejes.log $(LOGS)/shift_sol038.log
