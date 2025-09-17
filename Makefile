build:
	python setup.py build_ext -i

all:
	uv run python setup.py build_ext -i

check: all
	uv run pytest -s --cov

bench: all
	uv run pytest --codspeed

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy -p placeholder

html: all
	uv run mkdocs build
