all:
	python setup.py build_ext -i

check: all
	python -m pytest -s --cov

bench: all
	python -m pytest --codspeed

lint:
	ruff check .
	ruff format --check .
	mypy -p placeholder

html: all
	PYTHONPATH=$(PWD) python -m mkdocs build
