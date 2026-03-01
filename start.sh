#!/bin/bash
# Startup script for AWS Lightsail deployment

# Run with gunicorn on port 80 (requires sudo or configure Lightsail to allow port binding)
# For production: sudo ./start.sh
# Or without sudo on port 8000: gunicorn --bind 0.0.0.0:8000 --workers 2 app:app

gunicorn --bind 0.0.0.0:80 --workers 2 app:app
