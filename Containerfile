FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --upgrade pip

COPY pyproject.toml /app

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install .

COPY . /app

ENTRYPOINT ["python3"]
CMD ["main.py"]