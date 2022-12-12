.PHONY: deps test run docs
.DEFAULT_GOAL:= run

deps:
	python3 -m pip install -r requirements.txt

test:
	python3 -m pytest

run: test docs
	python3 main.py

docs:
	python3 -m pydoc -w grid render
	mv grid.html render.html docs/
