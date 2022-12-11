.PHONY: deps test run
.DEFAULT_GOAL:= run

deps:
	python3 -m pip install -r requirements.txt

test:
	python3 -m pytest

run: test
	python3 main.py

