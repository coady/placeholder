all: check
	make -C docs html SPHINXOPTS=-W

check:
	python3 setup.py $@ -ms
	black -q --check .
	flake8
	mypy -p placeholder
	pytest --cov --cov-fail-under=100
