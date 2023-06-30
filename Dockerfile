FROM python:3.11
LABEL maintainer="Vertyco#0117"

WORKDIR /app

# Put first so anytime this file changes other cached layers are invalidated.
COPY ./requirements.txt .
RUN pip install -U pip setuptools wheel
RUN pip install -r requirements.txt

COPY ./src ./src

ENV PYTHONPATH=/app/
ENV PYTHONUNBUFFERED=1
ENV HOST=127.0.0.1
ENV WORKERS=1

CMD python -m uvicorn src.api:app --host $HOST --port 8100 --workers $WORKERS
