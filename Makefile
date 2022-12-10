.PHONY: run deps
.DEFAULT_GOAL:= run

deps:
	python3 -m pip install -r requirements.txt

run:
	python3 main.py
