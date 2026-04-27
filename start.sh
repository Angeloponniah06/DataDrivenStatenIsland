#!/usr/bin/env bash
# Startup script for AWS Lightsail deployment

set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
BRANCH="${GIT_BRANCH:-main}"
HOST="${APP_HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
WORKERS="${WEB_CONCURRENCY:-2}"
APP_MODULE="${APP_MODULE:-app:app}"
VENV_DIR="${VENV_DIR:-${PROJECT_DIR}/venv}"
PIP_BIN="${PIP_BIN:-${VENV_DIR}/bin/pip}"
GUNICORN_BIN="${GUNICORN_BIN:-${VENV_DIR}/bin/gunicorn}"

cd "$PROJECT_DIR"

if [ -d .git ]; then
	echo "Synchronizing code from origin/${BRANCH}"
	git fetch origin "$BRANCH"
	git ls-files -z | grep -zv '^data\.db$' | xargs -0 -r git checkout "origin/${BRANCH}" --
	git clean -fd
fi

if [ ! -x "$GUNICORN_BIN" ]; then
	if [ -x "$PIP_BIN" ]; then
		"$PIP_BIN" install -r requirements.txt
	else
		echo "Virtual environment not found at $VENV_DIR" >&2
		exit 1
	fi
fi

export FLASK_SECRET_KEY="${FLASK_SECRET_KEY:-change-this-secret-key-in-production}"

echo "Starting ${APP_MODULE} on ${HOST}:${PORT} with ${WORKERS} worker(s)"
exec "$GUNICORN_BIN" --bind "$HOST:$PORT" --workers "$WORKERS" --timeout 120 --reload "$APP_MODULE"
