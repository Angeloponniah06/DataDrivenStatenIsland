#!/bin/bash
# Startup script for AWS Lightsail deployment

# Run with gunicorn on port 80 (requires sudo or configure Lightsail to allow port binding)
# For production: sudo ./start.sh
# Or without sudo on port 8000: gunicorn --bind 0.0.0.0:8000 --workers 2 app:app

# Defaults are safe for non-root users. Override with env vars when needed.
# Examples:
#   ./start.sh
#   PORT=8000 WEB_CONCURRENCY=2 ./start.sh
#   PORT=80 sudo ./start.sh

set -e

HOST="${APP_HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
WORKERS="${WEB_CONCURRENCY:-2}"
APP_MODULE="${APP_MODULE:-app:app}"
GUNICORN_BIN="${GUNICORN_BIN:-gunicorn}"

echo "Starting ${APP_MODULE} on ${HOST}:${PORT} with ${WORKERS} worker(s)"
exec "${GUNICORN_BIN}" --bind "${HOST}:${PORT}" --workers "${WORKERS}" --timeout 120 --reload "${APP_MODULE}"
