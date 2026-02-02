check:
	uv run python setup.py build_ext -i
	uv run pytest -s --cov

bench:
	uv run pytest --codspeed

lint:
	uvx ruff check
	uvx ruff format --check
	uvx ty check placeholder

html:
	uv run --group docs mkdocs build
