all:
	uv run python setup.py build_ext -i

check: all
	uv run pytest -s --cov

bench: all
	uv run pytest --codspeed

lint:
	uvx ruff check
	uvx ruff format --check
	uvx ty check placeholder

html: all
	uv run --group docs mkdocs build
