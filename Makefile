TEST_FLAGS ?= -v
COVER_FLAGS ?= --cov=app --cov-report=term-missing
APP_ENTRY ?= app.main:app

.PHONY: docker-up docker-clean test lint deps build clean format help run
.DEFAULT_GOAL := help

docker-up:
	docker compose up

docker-build:
	docker compose build

docker-clean:
	docker compose down
	docker image prune -f

test:
	poetry run pytest $(TEST_FLAGS) $(COVER_FLAGS)

lint:
	poetry run ruff check .
	poetry run ruff format --check .

format:
	poetry run ruff check --fix .
	poetry run ruff format .

deps:
	poetry install

build: deps
	poetry build

run:
	poetry run uvicorn $(APP_ENTRY) --host 0.0.0.0 --port 8080 --reload

clean:
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -f .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +

help:
	@echo "Доступные команды:"
	@echo "  docker-up    - Запустить контейнер Docker"
	@echo "  docker-clean - Остановить контейнеры и удалить старые образы"
	@echo "  docker-build - Собрать образ Docker"
	@echo "  test         - Запустить тесты с отчетом о покрытии"
	@echo "  lint         - Проверить код линтером (только проверка)"
	@echo "  format       - Отформатировать код и исправить ошибки"
	@echo "  deps         - Установить зависимости (через Poetry)"
	@echo "  build        - Собрать Python-пакет для дистрибуции"
	@echo "  run          - Запустить приложение локально"
	@echo "  clean        - Удалить кэш, временные файлы и артефакты"