install: .env
	poetry install

.env:
	@test ! -f .env && cp .env.example .env


lint:
	poetry run flake8

test:
	poetry run pytest -vvvv

check: test lint

migrate:
	poetry run alembic upgrade head

run: migrate
	poetry run python -m flask run

prod: migrate
	poetry run gunicorn --workers=4 --bind=127.0.0.1:5000 'page_analyzer:create_app()'

requirements:
	@poetry export -f requirements.txt -o requirements.txt

.PHONY: install test lint selfcheck check build