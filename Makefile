# SELENE PROTOCOL — единый раннер
# make setup | test [SEASON=01] [SERIES=s01e01] | project | links | route | series | check

SHELL := /bin/bash
PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

ifdef SERIES
TARGETS := $(wildcard season-*/$(SERIES)-*/tests)
else ifdef SEASON
TARGETS := $(wildcard season-$(SEASON)-*/s*/tests)
else
TARGETS := $(wildcard season-*/s*/tests)
endif

.PHONY: help setup test project links route series check

help:
	@echo "make setup                окружение .venv и pytest"
	@echo "make test                 все серии"
	@echo "make test SEASON=01       один сезон"
	@echo "make test SERIES=s01e01   одна серия"
	@echo "make project [SEASON=01] сквозной проект сезона из твоих артефактов"
	@echo "make links                битые ссылки между документами"
	@echo "make route                маршрут: 120 серий, оси, зависимости"
	@echo "make series               стандарт серий: эталон, каркас, неверные решения"
	@echo "make check                всё вместе, как перед публикацией"

setup:
	python3 -m venv .venv
	.venv/bin/python -m pip install --quiet -e '.[test]'

test:
	@$(PYTHON) -m pytest $(if $(TARGETS),$(TARGETS),$(error Серии не найдены)) -q

project:
	@SEASON=$(SEASON) $(PYTHON) tools/build_project.py

links:
	@$(PYTHON) tools/check_links.py

route:
	@$(PYTHON) tools/check_route.py

series:
	@$(PYTHON) tools/check_series.py

check: links route series project
