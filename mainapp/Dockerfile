# ----- build ai_logic ------
FROM python:3.8-slim

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN \
  pip install -U pip poetry && \
  apt-get update && \
  apt-get install -y build-essential && \
  poetry config virtualenvs.create false && \
  poetry install -n && \
  apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* 

COPY mainapp ./mainapp

EXPOSE 8001
CMD ["python", "-m", "mainapp"]
