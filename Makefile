run:
	gunicorn -w 4 simple_http.app:app

test:
	pytest -sv ./tests

ruff:
	ruff format .
	ruff check . --fix
