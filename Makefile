install:
	poetry install

lint:
	poetry run flake8 page_analyzer/

run:
	poetry run python -m flask run
