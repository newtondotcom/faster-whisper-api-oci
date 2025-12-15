#!/bin/bash
set -e

# Set defaults for gunicorn configuration
GUNICORN_BIND=${GUNICORN_BIND:-0.0.0.0:5000}
GUNICORN_WORKERS=${GUNICORN_WORKERS:-4}
GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-300}
GUNICORN_LOG_LEVEL=${GUNICORN_LOG_LEVEL:-info}

# Run gunicorn with proper signal handling
exec gunicorn \
    --bind "$GUNICORN_BIND" \
    --workers "$GUNICORN_WORKERS" \
    --timeout "$GUNICORN_TIMEOUT" \
    --access-logfile - \
    --error-logfile - \
    --log-level "$GUNICORN_LOG_LEVEL" \
    main:app

