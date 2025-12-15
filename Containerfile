FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY pyproject.toml /app

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install .

COPY . /app

COPY scripts/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/docker-entrypoint.sh"]