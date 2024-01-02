run:
	gunicorn -w 4 tests.dummy_app:app

test:
	pytest -sv ./tests

ruff:
	ruff format .
	ruff check . --fix
