
.PHONY: all, format, f, e, p

app=box_with_dovetail_lid.py

all:
	@echo "make <target>"
	@echo "targets:"
	@echo " f|format   # Format"
	@echo " e          # Run with cq-editor"
	@echo " p          # Run with python"
	@echo " t          # Run pytest"
	@echo " mypy       # Run mypy *.py"

p:
	@if [ "${app}" == "" ]; then echo "Expecting 'app=xxx'"; exit 1; fi
	python ${app}

e:
	@if [ "${app}" == "" ]; then echo "Expecting 'app=xxx'"; exit 1; fi
	cq-editor ${app}

format: f
f:
	isort *.py
	black *.py
	flake8 *.py

mypy:
	mypy *.py
	mypy
	mypy

t:
	pytest

clean:
	rm -rf generated/* __pycache__
