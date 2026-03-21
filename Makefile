run:
	docker compose run --rm app python main.py

test:
	docker compose run --rm app python -m unittest discover -s tests
