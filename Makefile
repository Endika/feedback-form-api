.PHONY: help install test test-unit test-integration test-all lint type-check format clean run docker-build docker-up

.DEFAULT_GOAL := help

help:
	@echo "📋 Feedback Form System - Comandos disponibles:"
	@echo ""
	@echo "🔧 Setup:"
	@echo "  make install          Instalar dependencias y configurar pre-commit hooks"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test             Ejecutar tests unitarios"
	@echo "  make test-integration Ejecutar tests de integración"
	@echo "  make test-all         Ejecutar todos los tests (unit + integration)"
	@echo "  make test-coverage    Ejecutar tests con reporte de cobertura"
	@echo ""
	@echo "✅ Code Quality:"
	@echo "  make lint             Ejecutar linter (Ruff)"
	@echo "  make type-check       Ejecutar type checker (mypy)"
	@echo "  make format           Formatear código (Ruff formatter)"
	@echo ""
	@echo "🚀 Ejecución:"
	@echo "  make run              Ejecutar servidor de desarrollo (uvicorn)"
	@echo ""
	@echo "🐳 Docker:"
	@echo "  make docker-build     Construir imagen Docker"
	@echo "  make docker-up        Iniciar contenedores con docker-compose"
	@echo ""
	@echo "🧹 Limpieza:"
	@echo "  make clean            Limpiar archivos generados (cache, builds, etc.)"
	@echo ""

install:
	poetry install
	poetry run pre-commit install

test:
	poetry run pytest tests/unit -v

test-integration:
	poetry run pytest tests/integration -v -m integration

test-all:
	poetry run pytest tests/ -v

test-coverage:
	poetry run pytest tests/ --cov

lint:
	poetry run ruff check .

type-check:
	poetry run mypy .

format:
	poetry run ruff format .

clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -r {} + 2>/dev/null || true
	rm -rf .coverage htmlcov dist build

run:
	poetry run uvicorn presentation.api.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t feedback-form-system:latest .

docker-up:
	docker-compose up -d
