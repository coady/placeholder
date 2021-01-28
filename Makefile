all:
	python3 setup.py build_ext -i

check: all
	pytest --cov

lint:
	python3 setup.py check -ms
	black --check .
	flake8
	mypy -p placeholder

html: all
	PYTHONPATH=$(PWD) mkdocs build

dist:
	python3 setup.py sdist bdist_wheel
	docker run --rm -v $(PWD):/usr/src -w /usr/src quay.io/pypa/manylinux2014_x86_64 make cp36 cp37 cp38 cp39

cp36 cp37:
	/opt/python/$@-$@m/bin/python setup.py build
	/opt/python/$@-$@m/bin/pip wheel . -w dist
	auditwheel repair dist/*$@m-linux_x86_64.whl

cp38 cp39:
	/opt/python/$@-$@/bin/python setup.py build
	/opt/python/$@-$@/bin/pip wheel . -w dist
	auditwheel repair dist/*$@-linux_x86_64.whl
