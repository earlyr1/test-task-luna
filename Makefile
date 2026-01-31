.PHONY: help up seed test down clean logs

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

up: ## Start project with seeding
	docker-compose up -d
	@echo "Waiting for DB to be healthy and migrated..."
	@until [ "$$(docker-compose ps api | grep '(healthy')" ]; do sleep 1; done
	@echo "DB is healthy! Running seed..."
	./seed.sql.sh -h localhost -U postgres -d app -p 5432 --password postgres
	@echo "Project is ready!"

test: ## Run tests
	docker-compose up -d db
	@echo "Waiting for API to be healthy..."
	@until [ "$$(docker-compose ps api | grep '(healthy')" ]; do sleep 1; done
	@echo "API is healthy! Running tests..."
	export DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/app && \
	uv lock && \
	uv sync && \
	uv run alembic upgrade head && \
	uv run pytest tests/

lint: ## Run linters
	uv run black . && \
    uv run isort . && \
	uv run mypy . && \
	uv run ruff check 

down: ## Stop all containers
	docker-compose down

clean: ## Stop containers and remove volumes
	docker-compose down -v

logs: ## Show logs
	docker-compose logs -f

logs-db: ## Show DB logs
	docker-compose logs -f db

logs-api: ## Show API logs
	docker-compose logs -f api