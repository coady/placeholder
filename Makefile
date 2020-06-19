all:
	python3 setup.py build_ext -i

check: all
	python3 setup.py $@ -ms
	black -q --check .
	flake8
	mypy -p placeholder
	pytest --cov --cov-fail-under=100

html: all
	make -C docs html SPHINXOPTS=-W

dist:
	python3 setup.py sdist bdist_wheel
	docker run --rm -v $(PWD):/usr/src -w /usr/src quay.io/pypa/manylinux2014_x86_64 make cp36 cp37 cp38

cp36 cp37:
	/opt/python/$@-$@m/bin/pip wheel . -w dist
	auditwheel repair dist/*$@m-linux_x86_64.whl

cp38:
	/opt/python/$@-$@/bin/pip wheel . -w dist
	auditwheel repair dist/*$@-linux_x86_64.whl
