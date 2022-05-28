all:
	python3 setup.py build_ext -i

check: all
	pytest -s --cov

lint:
	black --check .
	flake8
	mypy -p placeholder

html: all
	PYTHONPATH=$(PWD) mkdocs build
