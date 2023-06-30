FROM python:3.11
LABEL maintainer="Vertyco#0117"

WORKDIR /src

# Copy scripts to the folder
COPY /src /src
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -U pip setuptools wheel && \
    pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONPATH=/src/
ENV PYTHONUNBUFFERED=1

CMD [ "python", "-m", "uvicorn", "src.api:app", "--host", "${HOST}", "--workers", "${UVICORN_WORKERS}" ]
