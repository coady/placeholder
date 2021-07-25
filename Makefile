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
	docker run --rm -v $(PWD):/usr/src -w /usr/src quay.io/pypa/manylinux_2_24_x86_64 make cp37 cp38 cp39 cp310

cp37:
	/opt/python/$@-$@m/bin/python -m build -nw
	auditwheel repair dist/*$@m-linux_x86_64.whl

cp38 cp39 cp310:
	/opt/python/$@-$@/bin/python -m build -nw
	auditwheel repair dist/*$@-linux_x86_64.whl
