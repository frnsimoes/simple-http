run:
	gunicorn -w 4 app:app
test:
	pytest ./tests

push:
# Usage: e.g. make push branch=main
	pytest tests/ \
	&& ruff format . \
	&& git push origin $(branch)
