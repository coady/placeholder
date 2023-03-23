all:
	python setup.py build_ext -i

check: all
	pytest -s --cov

lint:
	black --check .
	ruff .
	mypy -p placeholder

html: all
	PYTHONPATH=$(PWD) python -m mkdocs build
