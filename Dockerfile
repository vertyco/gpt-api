FROM python:3.11
LABEL maintainer="Vertyco#0117"

WORKDIR /

# Copy scripts to the folder
COPY /src /src
COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh

# Install dependencies
RUN pip install -U pip setuptools wheel && \
    pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONPATH=/
ENV PYTHONUNBUFFERED=1
ENV HOST=127.0.0.1
ENV WORKERS=1

CMD python -m uvicorn src.api:app --host $HOST --workers $WORKERS
