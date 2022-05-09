.PHONY: all

SRC := ./asyncio_task_helpers
CMD := poetry run

all: install-deps pre-commit tox

test:
	$(CMD) pytest

tox:
	$(CMD) tox

pre-commit:
	$(CMD) pre-commit run --all-files

install-deps:
	poetry install
	$(CMD) pre-commit install
