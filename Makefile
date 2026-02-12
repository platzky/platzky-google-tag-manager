lint:
	poetry run black .
	poetry run ruff check --fix .

dev: lint
	poetry run pyright .

lint-check:
	poetry run black --check .
	poetry run ruff check .
	poetry run pyright .
	poetry run interrogate platzky_google_tag_manager/ --verbose

unit-tests:
	poetry run python -m pytest -v

coverage:
	poetry run coverage run --branch --source=platzky_google_tag_manager -m pytest -m "not skip_coverage"
	poetry run coverage report --fail-under=90
	poetry run coverage lcov

html-cov: coverage
	poetry run coverage html

audit:
	# Ignore deprecated 'py' package pulled in transitively; remove once no longer in dependency tree
	poetry audit --ignore-package=py

build:
	poetry build
