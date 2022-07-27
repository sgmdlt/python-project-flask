install:
	poetry install

lint:
	poetry run flake8 .

test:
	poetry run pytest -vvvv

check: test lint

run:
	poetry run python -m flask run

prod:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:5000 page_analyzer.app:app

requirements:
	@poetry export -f requirements.txt -o requirements.txt