all:
	python setup.py build_ext -i

check: all
	pytest -s --cov

lint:
	ruff .
	ruff format --check .
	mypy -p placeholder

html: all
	PYTHONPATH=$(PWD) python -m mkdocs build
