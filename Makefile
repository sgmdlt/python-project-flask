install:
	poetry install

lint:
	poetry run flake8 page_analyzer/

run:
	poetry run python -m flask run

prod:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:5000 page_analyzer.app:app
