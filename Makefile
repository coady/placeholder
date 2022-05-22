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

dist:
	python3 -m build -n
	docker run --rm -v $(PWD):/usr/src -w /usr/src quay.io/pypa/manylinux_2_24_x86_64 make wheel

wheel:
	python3.7 -m build -nw
	auditwheel repair dist/*-linux_x86_64.whl
