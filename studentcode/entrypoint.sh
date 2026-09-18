#!/bin/sh
set -e

echo "Waiting for PostgreSQL at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
while ! nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  sleep 1
done
echo "PostgreSQL is up."

# This service never runs migrations for shared tables - the admin_service
# owns the schema. We just collect static files and start the server.
python manage.py collectstatic --noinput --clear || true

echo "Starting Student Result Service on port 8000..."
exec python manage.py runserver 0.0.0.0:8000
