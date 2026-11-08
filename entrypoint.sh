#!/bin/sh
set -e

echo "Ejecutando migraciones de Alembic..."
alembic upgrade head

echo "Iniciando la aplicación..."
exec "$@"