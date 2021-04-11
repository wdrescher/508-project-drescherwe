# syntax=docker/dockerfile:1.0.0-experimental
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements.txt /requirements.txt

RUN --mount=type=ssh pip install -r /requirements.txt && \
  pip install urlparser && \
  rm -Rf /root/.cache && rm -Rf /tmp/pip-install*

COPY ./app /app
