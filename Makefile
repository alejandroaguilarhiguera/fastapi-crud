
.PHONY: install init-db migrate migration seed run up down clean

PYTHON := python3
PIP := $(PYTHON) -m pip
ALEMBIC := $(PYTHON) -m alembic

# Crear entorno virtual e instalar dependencias
install:
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r requirements.txt

# Inicializar Alembic (solo la primera vez)
init-db:
	.venv/bin/alembic init alembic

# Crear una nueva migración: make migration m="create products"
migration:
	.venv/bin/alembic revision --autogenerate -m "$(m)"

# Aplicar migraciones pendientes
migrate:
	.venv/bin/alembic upgrade head

# Revertir la última migración
rollback:
	.venv/bin/alembic downgrade -1

# Insertar productos de prueba
seed:
	.venv/bin/python -m scripts.seed_products

# Levantar FastAPI con recarga automática
run:
	.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Levantar PostgreSQL con Docker Compose
up:
	docker compose up -d

# Detener los contenedores
down:
	docker compose down

# Instalar, migrar y cargar datos
setup: install up migrate seed
