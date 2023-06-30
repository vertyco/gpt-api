FROM python:3.11
LABEL maintainer="Vertyco#0117"

WORKDIR /app

# Copy scripts to the folder
COPY src/ ./src
COPY requirements.txt .
COPY entrypoint.sh .

# Install dependencies
RUN pip install -U pip setuptools wheel && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV HOST=127.0.0.1
ENV WORKERS=1

CMD python -m uvicorn api:app --host $HOST --workers $WORKERS
