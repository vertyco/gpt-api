#!/bin/sh

# Start Uvicorn with $HOST, $PORT, $LOG_LEVEL and $WORKERS variables, if they are set
exec uvicorn src.api:app \
    --host ${HOST:-127.0.0.1} \
    --port ${PORT:-8000} \
    --workers ${UVICORN_WORKERS:-1}
