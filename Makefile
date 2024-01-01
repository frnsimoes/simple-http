run:
	gunicorn -w 4 simple_http.app:app
test:
	pytest -sv ./tests

push:
# Usage: e.g. make push branch=main
	pytest tests/ \
	&& ruff format . \
	&& git push origin $(branch)
