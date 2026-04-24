#!/bin/bash
# Startup script for AWS Lightsail deployment

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
exec "${GUNICORN_BIN}" --bind "${HOST}:${PORT}" --workers "${WORKERS}" --timeout 120 "${APP_MODULE}"
