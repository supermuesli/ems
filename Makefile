.PHONY: venv deps test docs run
.DEFAULT_GOAL:= run

BIN=$(CURDIR)/venv/bin

venv:
	python3 -m venv $(CURDIR)/venv

deps: venv
	$(BIN)/python3 -m pip install -r requirements.txt

test: deps
	$(BIN)/python3 -m pytest

docs:
	$(BIN)/python3 -m pydoc -w grid render
	mv grid.html render.html docs/

run: test docs
	$(BIN)/python3 main.py